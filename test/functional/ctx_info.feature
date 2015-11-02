Feature: context info
    The 'info' subcommand

    Background:
        Given I have a clean database

    Scenario: no current context
        When I invoke the command "ctx info"
        Then I should see "No active task"

    Scenario: show current context
        Given The current time is "2015-01-01 10:00:00"
        And I have an active task "TASK0" started at "2015-01-01 09:00:00"
        When I invoke the command "ctx info"
        Then I should see "task: TASK0"
        And I should see "total time: 1:00:00"
        And I should see "status: running"

    Scenario: show current context with custom format string
        Given The current time is "2015-01-01 10:00:00"
        And I have an active task "TASK0" started at "2015-01-01 09:00:00"
        When I invoke the command "ctx info -f {id}-{description}-{status}-{duration}"
        Then I should see "TASK0--running-1:00:00"
