
# database environment variables
# DATABSE_URL is set in heroku environment

# auth environment variables
export CALLBACK_URL="https://bt-kudos-app.herokuapp.com/"
export AUTH0_DOMAIN="fsndbtamas.eu.auth0.com"
export AUTH0_CLIENT_ID="mC5F8kIqdfb7sLgU4N6aPHAO1j3y3Iiw"
export AUTH0_SECRET="k-72M6lXU_h38qPcXb1i8FTHDS5pZzWL8tvNvVvDtedofXqG6I69-zZ12eJSMMuZ"
export API_AUDIENCE="https://kudos-app-auth/"

# JWTs for testing
# to obtain these JWTs login via the basic frontend on /
# test users:
#  - Manager: manager@manager.com, managerY3?
#  - Team-member: tm@tm.com, memberY3?

export MANAGER_JWT="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBpcGozWHNPbjFNbWdUcERUejdfNCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRidGFtYXMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNWU4NDA5NTI1ODEyMDA3MDNjNDhkYyIsImF1ZCI6Imh0dHBzOi8va3Vkb3MtYXBwLWF1dGgvIiwiaWF0IjoxNjAwMDk0Mjg2LCJleHAiOjE2MDAxODA2ODYsImF6cCI6Im1DNUY4a0lxZGZiN3NMZ1U0TjZhUEhBTzFqM3kzSWl3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6a3Vkb3MiLCJjcmVhdGU6dGVhbS1tZW1iZXIiLCJkZWxldGU6a3Vkb3MiLCJkZWxldGU6dGVhbS1tZW1iZXIiLCJnZXQ6dGVhbS1tZW1iZXJzIiwicGF0Y2g6a3Vkb3MiLCJyZWFkOmt1ZG9zIl19.BoCgovzFIYDENuYQVmdvm930qteoNDWlH6BuUdGaf03nJ7Q7Cngsydz0NxwldkihL6dCe8O0BhEEh4DXwLqKOyPP-8HL4WZ6HbFd-bmVw6st7XAh3_FTiK_ldKf538XTiVtYesGkiY_GYSKA0B8T9PBMUdUbB4KbU1jF17_agB6DRUN0wyrjf7KQSfXwBBdV-m6K-1JPRKp2a6hoBVXGqf99RwVxpLOLkvZ-nalDDXlryBoNoqwh6l_-dB9Y_wgLi91b_G8C1xduU8xfqT7sobqcksgVrg00EjpDV9rp2MoYuuSttsCduAb3hzT60CznJN08nSNf5OCIVLD-Lk7M3Q"
export TEAM_MEMBER_JWT="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBpcGozWHNPbjFNbWdUcERUejdfNCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRidGFtYXMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNWU5Y2U4MzE1NzI1MDA3NmM2ZDQ0YiIsImF1ZCI6Imh0dHBzOi8va3Vkb3MtYXBwLWF1dGgvIiwiaWF0IjoxNjAwMDcxNTY4LCJleHAiOjE2MDAxNTc5NjgsImF6cCI6Im1DNUY4a0lxZGZiN3NMZ1U0TjZhUEhBTzFqM3kzSWl3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6a3Vkb3MiLCJnZXQ6dGVhbS1tZW1iZXJzIiwicmVhZDprdWRvcyJdfQ.LIOudtG9tFSYz3uymV3agRUo2-0vypW3WGADj-KJYxMLUCpJofqAFt8wPW5wh-QPVoGw4W7eAbUKOEi6c07y43fjl5o-spH8x6g7qDHIzNzTrP0qCg5edBRt7G4FD1ZHcKQvf-LYB7bMqV5JglFtp1rQ-5l3Q_5iktjbSkoGFyNb4ghYuA6ggv6Nk8PgAEk3YgvSfgYIDRp3CqMRCtiQsqp_5ZgHjTcfo-aPlJtOoBavrWzUf1CAbtPLZ0mNGN4ElLszNGdXtcG5gPfEqKsSLKukSXLIcZZZ0fZyh9muUWHFgDd-y_dTCDaIulEK1EG6jWp3iDrMt3Leou9WYUc9bA"