Feature: context new
    The 'new' subcommand

    Background:
        Given I have a clean database

    Scenario: duplicate task id
        Given I have an active task "TASK0"
        When I invoke the command "ctx new TASK0"
        Then I should see "Cannot create task 'TASK0': Duplicate task ID"

    Scenario: create a new task
        Given I have an active task "TASK0"
        When I invoke the command "ctx new TASK1"
        Then I should see "Created task 'TASK1'"
        And The active task is "TASK0"

    Scenario: create a new task and switch to it
        Given The current time is "2015-01-01 10:00:00"
        And I have an active task "TASK0"
        When I invoke the command "ctx new -s TASK1"
        Then I should see "Created task 'TASK1'"
        And I should see "Switched to task 'TASK1'"
        And The active task is "TASK1"
        And The TASK0 should end at 2015-01-01 10:00:00
