# How to Create Tables in Railway MySQL

## Step 1: Add MySQL Database in Railway

1. **In your Railway project**, click **"+ New"**
2. **Select "Database"**
3. **Select "MySQL"**
4. Railway will create the database automatically

## Step 2: Get MySQL Connection Details

1. **Click on the MySQL service** in Railway
2. **Go to "Variables" tab**
3. **Copy these values:**
   - `MYSQLHOST`
   - `MYSQLPORT` (usually 3306)
   - `MYSQLDATABASE`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`

## Step 3: Connect to Railway MySQL

### Option A: Using DBeaver (Easiest)

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
6. **Open the file:** `railway_setup.sql` (in your project folder)
7. **Copy all the SQL** and paste it into DBeaver
8. **Run the script** (Ctrl+Enter or Cmd+Enter)

### Option B: Using Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Link to project:**
   ```bash
   railway link
   ```

4. **Connect to MySQL:**
   ```bash
   railway connect mysql
   ```

5. **Run SQL file:**
   ```bash
   mysql -h <MYSQLHOST> -u <MYSQLUSER> -p<MYSQLPASSWORD> <MYSQLDATABASE> < railway_setup.sql
   ```

## Step 4: Verify Tables Created

In DBeaver or Railway, run:
```sql
SHOW TABLES;
```

You should see:
- users
- tasks
- daily_plan
- categories
- notifications

## Step 5: Verify Users Created

```sql
SELECT username, role FROM users;
```

You should see:
- admin (role: admin)
- Vaishnavi, Student2, Student3, Student4 (role: user)

---

## That's It! ✅

Your Railway database now has all the tables and users, just like your local database!
