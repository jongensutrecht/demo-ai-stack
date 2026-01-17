# Security Invariant Discovery Questions

Gebruik deze vragen om security invarianten te ontdekken.

---

## Authentication

### Token/Session Management
- Welke endpoints zijn beveiligd met authenticatie?
- Mogen expired tokens OOIT geaccepteerd worden?
- Mogen invalid tokens OOIT resulteren in data access?
- Wat gebeurt er als een token halfway een request expired?

### Multi-factor Authentication
- Is MFA vereist voor bepaalde acties?
- Mag een MFA bypass OOIT mogelijk zijn?

**Typische invarianten:**
- `INV-SEC-001`: Protected endpoints NEVER return data without valid token
- `INV-SEC-002`: Expired tokens are NEVER accepted
- `INV-SEC-003`: MFA-required actions NEVER succeed without MFA

---

## Authorization

### Role-Based Access
- Welke rollen zijn er (user, admin, superadmin)?
- Welke acties zijn admin-only?
- Mag een user OOIT admin functies uitvoeren?

### Resource Ownership
- Welke resources zijn user-specific (orders, profiles, etc.)?
- Mag een user OOIT data van een andere user zien?
- Mag een user OOIT data van een andere user modificeren?

### Tenant Isolation (multi-tenant apps)
- Is er tenant isolation?
- Mag data van tenant A OOIT zichtbaar zijn voor tenant B?

**Typische invarianten:**
- `INV-SEC-010`: Admin endpoints are NEVER accessible without admin role
- `INV-SEC-011`: User data is NEVER exposed to other users
- `INV-SEC-012`: Tenant A data is NEVER accessible by Tenant B

---

## Data Protection

### Sensitive Data
- Welke data is gevoelig (passwords, tokens, PII)?
- Mag gevoelige data OOIT in logs verschijnen?
- Mag gevoelige data OOIT in error messages zitten?
- Mag gevoelige data OOIT in URLs zitten?

### Encryption
- Welke data moet encrypted opgeslagen worden?
- Mag plaintext OOIT in de database staan voor gevoelige velden?

### Data Retention
- Zijn er retention policies?
- Mag deleted data OOIT nog opvraagbaar zijn?

**Typische invarianten:**
- `INV-SEC-020`: Passwords are NEVER stored in plaintext
- `INV-SEC-021`: Sensitive data is NEVER logged
- `INV-SEC-022`: API keys are NEVER exposed in responses
- `INV-SEC-023`: PII is NEVER included in URLs

---

## Input Validation

### Injection Prevention
- Zijn er database queries met user input?
- Is er HTML rendering met user input?
- Zijn er command executions met user input?

### File Handling
- Kunnen users files uploaden?
- Mogen arbitrary file paths OOIT geaccepteerd worden?

**Typische invarianten:**
- `INV-SEC-030`: SQL injection is NEVER possible
- `INV-SEC-031`: XSS is NEVER possible in user input
- `INV-SEC-032`: Path traversal is NEVER possible
- `INV-SEC-033`: Command injection is NEVER possible

---

## API Security

### Rate Limiting
- Zijn er rate limits?
- Mag brute force OOIT mogelijk zijn?

### CORS
- Welke origins zijn toegestaan?
- Mag een unauthorized origin OOIT requests maken?

**Typische invarianten:**
- `INV-SEC-040`: Brute force is NEVER possible (rate limiting)
- `INV-SEC-041`: Unauthorized origins are NEVER allowed

---

## Questions to Ask User

```markdown
1. **Authentication**
   - Welke endpoints moeten ALTIJD authenticatie vereisen?
   - Zijn er publieke endpoints? Welke?

2. **Authorization**
   - Welke rollen zijn er in het systeem?
   - Welke acties zijn beperkt tot specifieke rollen?
   - Welke data is user-specific en mag NOOIT door anderen gezien worden?

3. **Sensitive Data**
   - Welke velden bevatten gevoelige informatie?
   - Mag deze data in logs verschijnen? (verwacht: NEE)
   - Moet deze data encrypted opgeslagen worden?

4. **Input Validation**
   - Zijn er bekende injection risico's?
   - Kunnen users files uploaden? Wat voor types?

5. **API Security**
   - Zijn er rate limits? Zo ja, wat zijn de limieten?
   - Welke externe origins mogen de API aanroepen?
```

---

## Discovery Commands

```bash
# Find auth middleware/decorators
rg "@require_auth|@login_required|@jwt_required|protected|middleware" --type py
rg "useAuth|isAuthenticated|authGuard|protectedRoute" --type ts

# Find role checks
rg "is_admin|role.*admin|hasRole|checkPermission" --type py
rg "isAdmin|hasPermission|checkRole" --type ts

# Find user-specific queries
rg "user_id.*=|owner_id.*=|created_by.*=" --type py
rg "userId.*===|ownerId.*===|createdBy" --type ts

# Find sensitive data handling
rg "password|secret|api_key|token|ssn|credit_card" --type py

# Find logging
rg "logger\.|log\.|console\.log" --type py --type ts

# Find SQL queries
rg "execute\(|query\(|raw\(|cursor\." --type py
rg "\.query\(|\.execute\(" --type ts
```
