from troposphere import Base64, Select, GetAtt, GetAZs, Join, Output, If, And, Not, Or, Equals, Condition
from troposphere import Parameter, Ref, Tags, Template
from troposphere.cloudformation import Init
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior
from troposphere.ec2 import PortRange
from troposphere.ec2 import SecurityGroup
from troposphere.ec2 import Instance, NetworkInterfaceProperty, PrivateIpAddressSpecification


t = Template()

t.add_description("""\
AWS CloudFormation Sample Template EC2InstanceWithSecurityGroupSample: Create an Amazon EC2 instance running the Amazon Linux AMI. The AMI is chosen based on the region in which the stack is run. This example creates an EC2 security group for the instance to give you SSH access. **WARNING** This template creates an Amazon EC2 instance. You will be billed for the AWS resources used if you create a stack from this template.""")
SSHLocation = t.add_parameter(Parameter(
    "SSHLocation",
    ConstraintDescription="must be a valid IP CIDR range of the form x.x.x.x/x.",
    Description="The IP address range that can be used to SSH to the EC2 instances",
    Default="0.0.0.0/0",
    MinLength="9",
    AllowedPattern="(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})",
    MaxLength="18",
    Type="String",
))

KeyName = t.add_parameter(Parameter(
    "KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair.",
    Type="AWS::EC2::KeyPair::KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH access to the instance",
))

InstanceType = t.add_parameter(Parameter(
    "InstanceType",
    Default="t2.small",
    ConstraintDescription="must be a valid EC2 instance type.",
    Type="String",
    Description="WebServer EC2 instance type",
    AllowedValues=["t1.micro"]
))

ImageId = t.add_parameter(Parameter(
    "ImageId",
    Type="String",
    Description="Image ID",
    ConstraintDescription="You must include an image ID."
))

InstanceSecurityGroup = t.add_resource(SecurityGroup(
    "InstanceSecurityGroup",
    SecurityGroupIngress=[
        {
            "ToPort": "22", 
            "IpProtocol": "tcp", 
            "CidrIp": Ref(SSHLocation), 
            "FromPort": "22" 
        }
    ],
    GroupDescription="Enable SSH access via port 22",
))

EC2Instance = t.add_resource(Instance(
    "EC2Instance",
    KeyName=Ref(KeyName),
    SecurityGroups=[Ref(InstanceSecurityGroup)],
    InstanceType=Ref(InstanceType),
    ImageId=Ref(ImageId),
))

InstanceId = t.add_output(Output(
    "InstanceId",
    Description="InstanceId of the newly created EC2 instance",
    Value=Ref(EC2Instance),
))

PublicDNS = t.add_output(Output(
    "PublicDNS",
    Description="Public DNSName of the newly created EC2 instance",
    Value=GetAtt(EC2Instance, "PublicDnsName"),
))

AZ = t.add_output(Output(
    "AZ",
    Description="Availability Zone of the newly created EC2 instance",
    Value=GetAtt(EC2Instance, "AvailabilityZone"),
))

PublicIP = t.add_output(Output(
    "PublicIP",
    Description="Public IP address of the newly created EC2 instance",
    Value=GetAtt(EC2Instance, "PublicIp"),
))

print(t.to_json())
