from ec2.vpc import VPC
from ec2.ec2 import EC2
from client_locator import EC2Client

def main():
    # Create a VPC 
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)
    
    vpc_response = vpc.create_vpc()
    print('VPC created:' + str(vpc_response))
    
    #Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    
    print('Added'+ vpc_name + ' to ' + vpc_id)
    
    
    # Create an IGW
    igw_response = vpc.create_internet_gateway()
    
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    
    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    
    # Create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    print('Subnet created for VPC ' + vpc_id + ':' + str(public_subnet_response))
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']

    # Add name tag to public subnet
    vpc.add_name_tag(public_subnet_id, 'Boto3-Public-Subnet')

    #Create a public Route Table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    print('Public Route Table created ' + vpc_id)
    
    # get route Table Id
    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    
    # Adding the IGW to public Route Table
    vpc.create_igw_route_to_public_route_table(rtb_id, vpc_id)
    
    # Associate Public Subnet with Route Table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)
    
    # Allow auto-assign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)
    
    # Create a Private Subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    print('Created private subnet ' + private_subnet_id + ' for VPC ' + vpc_id)
     
    # Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, 'Boto3-Private-Subnet')
    
    
    # EC2 Instances
    ec2 = EC2(ec2_client)
    
    # Create a key pair    
    key_pair_name = 'Boto3-KeyPair'
    key_pair_response = ec2.create_key_pair(key_pair_name)
    print('Created Key Pair with name ' + key_pair_name + ':' + str(key_pair_response))
    
    # Create a security group
    public_security_group = 'Boto3-Public-SG'
    public_security_group_description = 'Public Security Group for Public Subnet Internet Access'
    ec2.create_security_group(public_security_group, public_security_group_description, vpc_id)
if __name__ == '__main__':
    main()