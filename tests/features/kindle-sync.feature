Feature: As a Kindle Cloud user
I want to be able to extract all of my book data
So that I can sync it with Goodreads
    
Background:
  Given I am using kindle-sync

Scenario: login to Kindle web reader
  Given user credentials
  Then log in to kindle cloud reader