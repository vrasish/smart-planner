# Export Database from DBeaver to Railway

## Step 1: Export from DBeaver

### Method A: Export All Tables (Recommended)

1. **Open DBeaver**
2. **Right-click on your `smartplanner` database**
3. **Select "Tools" → "Export Data"**
4. **Choose "SQL" format**
5. **Select all tables:**
   - `users`
   - `tasks`
   - `daily_plan`
   - `categories`
   - `notifications`
6. **Click "Next"**
7. **Choose export options:**
   - ✅ Include CREATE statements
   - ✅ Include DROP statements
   - ✅ Include INSERT statements (if you want data)
8. **Click "Start"**
9. **Save the file** as `smartplanner_export.sql`

### Method B: Export Structure Only (Faster)

1. **Right-click on `smartplanner` database**
2. **Select "Tools" → "Generate SQL" → "DDL"**
3. **Select all tables**
4. **Click "Generate"**
5. **Copy the SQL** or save to file

### Method C: Use Command Line (Alternative)

If you have MySQL command line access:

```bash
mysqldump -u root -p smartplanner > smartplanner_export.sql
```

---

## Step 2: Add MySQL Database in Railway

1. **In Railway project**, click **"+ New"**
2. **Select "Database"**
3. **Select "MySQL"**
4. Railway will create the database automatically

---

## Step 3: Get Railway MySQL Connection Info

1. **Click on the MySQL service** in Railway
2. **Go to "Variables" tab**
3. **Note these values:**
   - `MYSQLHOST`
   - `MYSQLPORT` (usually 3306)
   - `MYSQLDATABASE`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`

---

## Step 4: Import SQL to Railway MySQL

### Option A: Using Railway CLI (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Link to your project:**
   ```bash
   railway link
   ```

4. **Connect to MySQL:**
   ```bash
   railway connect mysql
   ```

5. **Import your SQL file:**
   ```bash
   mysql -h <MYSQLHOST> -u <MYSQLUSER> -p<MYSQLPASSWORD> <MYSQLDATABASE> < smartplanner_export.sql
   ```

### Option B: Using DBeaver to Connect to Railway

1. **In DBeaver**, click **"New Database Connection"**
2. **Select "MySQL"**
3. **Enter Railway credentials:**
   - Host: `<MYSQLHOST>` (from Railway)
   - Port: `3306`
   - Database: `<MYSQLDATABASE>`
   - Username: `<MYSQLUSER>`
   - Password: `<MYSQLPASSWORD>`
4. **Test connection** → Click "Finish"
5. **Right-click on the Railway database** → "SQL Editor" → "New SQL Script"
6. **Paste your exported SQL**
7. **Run the script** (Ctrl+Enter or Cmd+Enter)

### Option C: Use Railway's Built-in SQL Editor

1. **Click on MySQL service** in Railway
2. **Go to "Data" tab** (if available)
3. **Or use "Query" tab** to run SQL

---

## Step 5: Run Setup Scripts (Alternative)

Instead of exporting, you can run your setup scripts:

1. **Set environment variables** in Railway backend service:
   ```
   DB_HOST = <MYSQLHOST>
   DB_PORT = 3306
   DB_NAME = <MYSQLDATABASE>
   DB_USER = <MYSQLUSER>
   DB_PASSWORD = <MYSQLPASSWORD>
   ```

2. **Use Railway CLI to run scripts:**
   ```bash
   railway run python setup_users.py
   railway run python setup_extended_features.py
   ```

---

## Quick Summary

1. **Export from DBeaver** → Save as `smartplanner_export.sql`
2. **Add MySQL in Railway** → Get connection details
3. **Import SQL** → Use Railway CLI or DBeaver to connect to Railway MySQL
4. **Done!** → Tables are now in Railway
