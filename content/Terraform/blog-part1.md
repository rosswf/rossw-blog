Title: Blog Setup - Part 1 - Provisioning with Terraform
Date: 2021-04-04 11:22
Tags: blog, meta, terraform
Summary: First post in a mini series detailing how this blog was setup. This one covers provisioning EC2 instances with terraform.
Slug: blog-setup-part1-terraform

This is the first part of a mini series detailing how this blog was setup. In this part I will discuss provisioning using Terraform. The relevant files can be found in this github [repo](https://github.com/rosswf/rossw-blog-terraform).

I have used a single AWS EC2 instance running ubuntu for hosting the actual content and Cloudflare for my DNS. I know this is slightly overkill for serving static web content but it was partially done this way as a learning exercise and this size of instance is available in the free tier. Even after the free period it isn't that expensive.

The aim of this is to discuss the process of setting up this blog, it is not to provide a guide on how to setup/install Terraform and setup your AWS credentials, there are plenty of resources available elsewhere for this, including the Terraform documentation. That said, the files in the github repo can be used as boiler-plate for provisioning your own EC2 instance for hosting web content.
I do not pretend to be an expert on terraform as I'm still learning,I have tried to follow [best practices](https://www.terraform-best-practices.com/) where possible but if anybody has any suggestions then please get in touch. 
Disclaimers aside, let's get into it!

### Preparation
There is a little bit of preparation required before creating the actual resources. 

<span style="color: grey">**backend.tf**</span>

    :::tf
    terraform {
        backend "s3" {
            bucket  = "rossw-backend"
            key     = "rossw-blog.tfstate"
            region  = "eu-west-2"
        }
    }

First of all we define a backend to store the state. It's a good idea to use an external source for this rather than storing it locally since if it is ever lost then terraform will have no idea what the state is and will end up creating resources again.
For this I have created an s3 bucket on AWS that we can simply point terraform to.


<span style="color: grey">**provider.tf**</span>

    :::tf
    terraform {
        required_providers {
            cloudflare = {
            source = "cloudflare/cloudflare"
            version = "~> 2.0"
            }
        }
    }

    provider "aws" {
        region = var.region
    }

    provider "cloudflare" {
    }

Next we define the providers, for this we will use both aws and cloudflare for automatically creating the appropriate DNS records since we won't know the IP address of the EC2 instance until it has been created.

<span style="color: grey">**output.tf**</span>

    :::tf
    output "ip_address" {
        value = aws_eip.server_ip.public_ip
    }

As mentioned above we won't know the IP address until creation so let's define an output to easily access this. It will come in handy in the next part when we look at ansible.

<span style="color: grey">**variables.tf**</span>

    :::tf
    variable "type" {
        type = string
        default = "t2.micro"
    }

    variable "region" {
        type = string
        default = "eu-west-2"
    }

    variable "number" {
        type = string
        default = "1"
    }

    variable "key_name" {
        type = string
    }

    variable "public_key" {
        type = string
    }

    variable "zone_id" {
        type = string
    }

    variable "my_public_ip" {
        type = string
    }

<span style="color: grey">**terraform.tfvars**</span>

    :::tf
    type = "t2.micro"
    region = "eu-west-2"
    number = "1"
    key_name = "rossw-key"

Finally let's define our variables and set values for some of them in terraform.tfvars.

<span style="color: grey">**vars.sh**</span>

    :::sh
    export CLOUDFLARE_API_KEY='your_cloudflare_api_key'
    export CLOUDFLARE_ACCOUNT_ID='your_cloudflare_account_id'
    export CLOUDFLARE_EMAIL='your_cloudflare_email'
    export TF_VAR_zone_id='your_cloudflare_zone_id'
    export TF_VAR_public_key='your_public_ssh_key'
    export TF_VAR_my_public_ip='your_public_ip_at_home'

The remaining variables are secret so will be set as environment variables. To make this easier I've created a bash script that I can run prior to terraform but you can set them up however you'd like.

### Resources

Now that everything is setup. Let's define our resources.

<span style="color: grey">**main.tf**</span>

    :::tf
    resource "aws_instance" "blog_web_server" {
        ami             = "ami-096cb92bb3580c759"
        instance_type   = var.type
        key_name        = var.key_name
        vpc_security_group_ids = [aws_security_group.blog_security_group.id]

        tags = {
            Name = "Blog Web Server"
        } 
    }

    resource "aws_key_pair" "blog_key" {
        key_name        = var.key_name
        public_key      = var.public_key
    }

    resource "aws_security_group" "blog_security_group" {
        name            = "Blog Web Server"
        description     = "Allow web and local SSH"

        ingress {
            from_port   = 80
            to_port     = 80
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        ingress {
            from_port   = 443
            to_port     = 443
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        ingress {
            from_port   = 22
            to_port     = 22
            protocol    = "tcp"
            cidr_blocks = ["${var.my_public_ip}/32"]
        }

        egress {
            from_port   = 0
            to_port     = 0
            protocol    = "-1"
            cidr_blocks = ["0.0.0.0/0"]
        }
    }

    resource "aws_eip" "server_ip" {
        vpc = true
        instance = aws_instance.blog_web_server.id
    }

    resource "cloudflare_record" "blog_root" {
        zone_id     = var.zone_id
        name        = "@"
        value       = aws_eip.server_ip.public_ip
        type        = "A"
        ttl         = 1
        proxied     = true

        depends_on = [
            aws_eip.server_ip,
        ]
    }

    resource "cloudflare_record" "blog_www" {
        zone_id     = var.zone_id
        name        = "www"
        value       = aws_eip.server_ip.public_ip
        type        = "A"
        ttl         = 1
        proxied     = true

        depends_on = [
            aws_eip.server_ip,
        ]
    }

Here we have:

- The EC2 instance, that will use the ubuntu 20.04 image.
- A key pair using our public ssh key defined earlier, this is used to access the instance via SSH.
- A security group. Port 80 and 443 are open to the world for serving the web content, while port 22 will only be accessible from our local machine, using the ip defined in the `TF_VAR_my_public_up` environment variable. Connections from any other IP address will be denied.
- An elastic IP for associating with your EC2 instance, that way if the instance goes down or we have to destroy it and create a new one the IP address won't change
- Cloudflare DNS records using the public IP address that gets given to the instance.

### Final Steps

A quick holy trinity of `terraform init`, `terraform plan`, `terraform apply` and we have a fully provisioned EC2 instance only allowing the connections we want and DNS records pointing to the instance! 

![AWS Console]({static}/images/part1-aws-console.png)

That's it for part1. In the next I will discuss configuring the server using ansible.

If you have any questions or would like me to go into more detail on anything discussed here please get in touch on twitter or e-mail me. Contact details be found [here]({filename}/pages/about.md).