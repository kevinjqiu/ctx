Feature: context stop
    The 'stop' subcommand

    Background:
        Given I have a clean database

    Scenario: no active task
        When I invoke the command "ctx stop"
        Then I should see "No active task"

    Scenario: task not running
        Given I have a stopped task "TASK0"
        When I invoke the command "ctx stop"
        Then I should see "Current task is not running"

    Scenario: with running task
        Given I have an active task "TASK1" started at "2015-10-01 08:30:00"
        And The current time is "2015-10-01 10:00:00"
        When I invoke the command "ctx stop"
        Then TASK1 should end at 2015-10-01 10:00:00
