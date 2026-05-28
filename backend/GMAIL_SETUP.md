# Gmail SMTP Setup Guide

## Step 1: Enable 2-Factor Authentication on Google Account
1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Click "2-Step Verification"
3. Follow the setup process

## Step 2: Create App Password
1. Go back to Security settings
2. Scroll down to "App passwords" (only visible if 2FA is enabled)
3. Select "Mail" and "Windows Computer"
4. Google will generate a 16-character password
5. Copy this password (you'll use it in the next step)

## Step 3: Configure .env File
1. Copy `.env.example` to `.env`
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your Gmail credentials:
   ```
   GMAIL_EMAIL=your-email@gmail.com
   GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

Replace:
- `your-email@gmail.com` - Your Gmail address
- `xxxx xxxx xxxx xxxx` - The 16-character app password from Step 2

## Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Run the Backend
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing
1. Go to `http://localhost:4200/signup`
2. Sign up with your email
3. Check your Gmail inbox for the verification code
4. Enter the code to verify

## Troubleshooting

### "Gmail authentication failed"
- Make sure you used the **16-character app password**, not your regular password
- Verify 2-Factor Authentication is enabled
- Check that GMAIL_EMAIL and GMAIL_PASSWORD are correct in `.env`

### "Less secure app access"
- You don't need this if you're using an App Password
- Gmail SMTP via App Password is the recommended method

### Email not arriving
- Check spam/junk folder
- Verify Gmail credentials in `.env`
- Check backend logs for error messages
