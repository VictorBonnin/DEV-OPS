# Groupe de sécurité pour l'instance EC2
# Ce groupe de sécurité va nous permettre de communiquer à l'intérieur et à l'extérieur de l'instance. On ajoute donc le port personnalisé TCP "0.0.0.0/0" pour autoriser toutes les IP à se conencter dessus.
# On va libérer et rendre accessible les ports de l'instance sur lesquels tournent nos services/conteneurs, pour ensuite qu'on puisse communqiuer avec (lancer graphana, prometheus, ...)

resource "aws_security_group" "ml_server_sg" {
  name        = "ml-server-sg"
  description = "Security group for ML server, allows TCP 5000, 9090, 3000, and SSH"

  # Règle pour SSH (port 22)
  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Règle pour le port 5000 (ML API)
  ingress {
    description = "Allow TCP port 5000"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Règle pour le port 9090 (Prometheus)
  ingress {
    description = "Allow Prometheus on port 9090"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Règle pour le port 3000 (Grafana)
  ingress {
    description = "Allow Grafana on port 3000"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Règle pour autoriser tout le trafic sortant
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ml-server-sg"
  }
}

# Instance EC2 avec le groupe de sécurité. Cela va ensuite nous permettre de créer une adresse IP élastique.
resource "aws_instance" "ml_server" {
  ami                    = "ami-0e2c8caa4b6378d8c"  # Remplacez avec un ID AMI valide pour votre région
  instance_type          = "t2.micro"
  key_name               = "testcleAMI"            # Paire de clés pour la connexion SSH
  vpc_security_group_ids = [aws_security_group.ml_server_sg.id]  # Attacher le groupe de sécurité

  user_data = <<-EOF
    #!/bin/bash
    apt update -y
    apt install -y docker.io
    systemctl start docker
    systemctl enable docker
  EOF

  tags = {
    Name = "ML-Server"
  }
}

# Associer l'IP élastique à l'instance, pour qu'on puisse requêter plus facilement et se connecter plus facilement avec toujours la même IP.
resource "aws_eip" "ml_server_eip" {
  instance = aws_instance.ml_server.id
  domain   = "vpc"  # Remplacement de vpc = true

  tags = {
    Name = "ml-server-eip"
  }
}
