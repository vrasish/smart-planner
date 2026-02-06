# Quick Export from DBeaver

## In DBeaver:

1. **Right-click on `smartplanner` database**
2. **Select "Tools" → "Export Data"**
3. **Format: SQL**
4. **Select all tables:**
   - users
   - tasks  
   - daily_plan
   - categories
   - notifications
5. **Options:**
   - ✅ CREATE statements
   - ✅ INSERT statements (if you have data)
6. **Export** → Save as `smartplanner_export.sql`

## Then import to Railway MySQL (see below)
