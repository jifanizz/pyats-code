*** Settings ***
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot
Library        unicon.robot.UniconRobot
#Variables      Config.yaml
Suite setup    Setup

*** Variables ***
${testbed}    ./xr-tb-1.yaml

*** Test Cases ***
Verify Interface Interface Operational Status
    ${output}=    execute "show interfaces Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}    line protocol is up

Verify Interface CRC Errors
    ${output}=    execute "show interfaces Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}    , 0 CRC

Verify Interface Drops
    ${output}=    execute "show interfaces Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}    0 total input drops

Verify OSPF Neighbor
    ${output}=    execute "show ospf neighbor Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}  FULL

Verify ISIS Neighbor
    ${output}=    execute "show isis neighbor Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}  Up

Verify MPLS Status
    ${output}=    execute "show mpls ldp neighbor Gi0/0/0/0" on device "xr1"
    Should Contain  ${output}  State: Oper

*** Keywords ***
Setup
    use genie testbed "${testbed}"
    connect to devices "xr1"
