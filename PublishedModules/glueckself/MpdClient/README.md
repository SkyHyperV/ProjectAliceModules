# MpdClient
### Download
##### > WGET method
```bash
wget http://modules.projectalice.ch/MpdClient -O ~/ProjectAlice/system/moduleInstallTickets/MpdClient.install
```
##### > Alice CLI method
```bash
./alice add module glueckself MpdClient
```
### Description
Control an MPD server

- Version: 0.0.17
- Author: glueckself
- Maintainers: maxbachmann
- Alice minimum Version: 1.0.0-a3
- Conditions:
  - en
  - de
- Pip requirements: python-mpd2
- System requirements: N/A

### Configuration
`mpdHost`:
 - type: `string`

`mpdPort`:
 - type: `int`

`mpdPassword`:
 - type: `string`
