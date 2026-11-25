# CECControl
Created this to manage my soundbar through Home Assistant, still work in progress though.

## Set-up on host device

Clone repo: `git clone https://github.com/m-thyl/CECControl`

Create token: `openssl rand -hex 32`

Replace placeholder token in server.py: `sudo nano /CECControl/opt/cec-control/server.py`

Make server.py only readable for root: `sudo chmod 600 /CECControl/opt/cec-control/server.py`

Copy to right folder: `sudo cp -r ~/CECControl/opt/cec-control /opt/`

Copy service: `sudo cp ~/CECControl/etc/systemd/system/cec-control.service /etc/systemd/system/`

Remove repo: `sudo rm -r ~/CECControl/`

Activate service: `sudo systemctl daemon-reload`

`sudo systemctl enable --now cec-control`

Check with: `sudo systemctl status cec-control`

## Set-up in Home Assistant

Add to secrets.yaml: `cec-control_auth: "Bearer REPLACE_WITH_GENERATED_TOKEN"`
*Keep the word Bearer within the token string*

Add to configuration.yaml in Home Assistant:
*change hostname*
```
rest_command:
  cec-control_on:
    url: "http://sendspin.local:8765/command"
    method: POST
    headers:
      Authorization: !secret cec-control_auth
    content_type: "application/json"
    payload: '{"command":"on"}'

  cec-control_off:
    url: "http://sendspin.local:8765/command"
    method: POST
    headers:
      Authorization: !secret cec-control_auth
    content_type: "application/json"
    payload: '{"command":"off"}'

  cec-control_volume_up:
    url: "http://sendspin.local:8765/command"
    method: POST
    headers:
      Authorization: !secret cec-control_auth
    content_type: "application/json"
    payload: '{"command":"volume_up"}'

  cec-control_volume_down:
    url: "http://sendspin.local:8765/command"
    method: POST
    headers:
      Authorization: !secret cec-control_auth
    content_type: "application/json"
    payload: '{"command":"volume_down"}'

  cec-control_mute:
    url: "http://sendspin.local:8765/command"
    method: POST
    headers:
      Authorization: !secret cec-control_auth
    content_type: "application/json"
    payload: '{"command":"mute"}'
```
