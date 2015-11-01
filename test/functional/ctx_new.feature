Feature: context new
    The 'new' subcommand

    Scenario: 'ctx new' will create a new task
        When I invoke the command "ctx new TASK1"
        Then I should see "Created task 'TASK1'"
