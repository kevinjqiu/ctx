Feature: context start
    The 'start' subcommand

    Background:
        Given I have a clean database

    Scenario: no active task
        When I invoke the command "ctx start"
        Then I should see "No active task"

    Scenario: task is already running
        Given I have a running task "TASK0"
        When I invoke the command "ctx start"
        Then I should see "Current task is already running"

    Scenario: with stopped task
        Given I have a stopped task "TASK1"
        And The current time is "2015-10-01 10:00:00"
        When I invoke the command "ctx start"
        Then TASK1 should start at 2015-10-01 10:00:00
