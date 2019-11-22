Feature: As a website owner,
            I want to secure my website

    Scenario: Successful Register
        Given flaskr is setup
        When i login with "admin@gmail.com" and "Admin123"
        Then i should see the alert "Your registration was successful!"


    Scenario: Incorrect Username
        Given flaskr is setup
        When i login with "monty" and "default"
        Then i should see the alert "Invalid email"

    Scenario: Incorrect Password
        Given flaskr is setup
        When i login with "admin@gmail.com" and "nka"
        Then  i should see the alert "Your password must contain at least one lowercase letter, one capital letter and one number, 8-30 characters long"
