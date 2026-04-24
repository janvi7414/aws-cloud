

Created a VPC with two route tables (private i.e. without IGW and public i.e. with IGW) associated with 4 subnets (2 private, 2 public)
, inside two availability zones.

link to video:
Configuration details:
- CIDR Block: 172.10.10.0/24
- Subnets:	subnet-01-public
		subnet-02-private
		subnet-03-public
		subnet-04-private
- Availabilty zones:	Ap-south-1a
			Ap-south-1b
- Gateways: Internet Gateway attached to Custon VPC. 
- Routing Logic: From each AZ one subnet is connect to private Route table and to public Route Table.
