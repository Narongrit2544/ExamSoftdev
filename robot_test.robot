*** Settings ***
Library           RequestsLibrary

*** Variables ***
${BASE_URL}      http://127.0.0.1:5000

*** Test Cases ***
Check Prime Number True
    [Documentation]    Verify that 29 is a prime number
    Create Session    mysession    ${BASE_URL}
    ${response}=    GET On Session    mysession    /is_prime/29
    Should Be Equal    ${response.json()['is_prime']}    ${True}

Check Prime Number False
    [Documentation]    Verify that 1 is not a prime number
    Create Session    mysession    ${BASE_URL}
    ${response}=    GET On Session    mysession    /is_prime/1
    Should Be Equal    ${response.json()['is_prime']}    ${False}
