# NetScout API

## Mission Briefing

Your API key is your clearance level. Use it wisely.

```
Authorization: Bearer your_api_key
```

## Operation Zones

### User Intelligence
```
GET /users/me
```
Extract your profile data. Clean and precise.

### Device Recon
```
GET /devices
```
Full inventory of your operational units.

```
GET /devices/{device_id}
```
Deep dive into specific unit specs. Access restricted to your command.

### Connection Protocol
```
POST /connection-codes
```
Generate secure handshake codes. Your devices, your rules.

### Report Analysis
```
POST /reports
```
Feed the system with device intel. Requires unit-level clearance.

```
GET /reports
```
Access your complete mission log.

```
GET /reports/device/{device_id}
```
Extract specific unit's operational history.

```
GET /reports/{report_id}
```
Retrieve detailed mission report. Eyes only.

## Status Codes

- 200: Mission accomplished
- 401: Clearance denied
- 403: Access restricted
- 404: Target not found
- 500: System compromised

Error responses contain mission-critical intel in the `detail` field.

---

**NetScout — Scan. Analyze. Take control** 
