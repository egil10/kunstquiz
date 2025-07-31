# Analytics Setup for Kunstquiz

This guide will help you set up comprehensive analytics tracking for your Kunstquiz application.

## 🎯 What We're Tracking

The analytics system tracks these key metrics:

1. **Games played** - Each time someone starts a new quiz
2. **Location** - Country/city based on IP address
3. **Total correct answers** - Aggregate correct responses
4. **Total wrong answers** - Aggregate incorrect responses
5. **Perfect scores** - 10/10 achievements
6. **Category preferences** - Which categories users choose
7. **Session duration** - How long users stay on the site
8. **Returning vs new users** - User engagement patterns
9. **Device/browser types** - Technical demographics
10. **User engagement** - Time on site, pages viewed

## 🚀 Quick Setup (Google Analytics 4)

### Step 1: Create Google Analytics Account

1. Go to [Google Analytics](https://analytics.google.com/)
2. Click "Start measuring"
3. Create a new account for your project
4. Create a new property called "Kunstquiz"
5. Choose "Web" as your platform
6. Enter your website URL (e.g., `https://yourusername.github.io/kunstquiz/`)

### Step 2: Get Your Measurement ID

1. In your Google Analytics property, go to **Admin** → **Data Streams**
2. Click on your web stream
3. Copy the **Measurement ID** (starts with `G-`)

### Step 3: Update Your Code

1. Open `index.html`
2. Find this line: `gtag('config', 'G-XXXXXXXXXX', {`
3. Replace `G-XXXXXXXXXX` with your actual Measurement ID

### Step 4: Deploy and Test

1. Commit and push your changes to GitHub
2. Wait for GitHub Pages to deploy
3. Visit your site and play a few games
4. Check Google Analytics Real-Time reports to see data coming in

## 📊 Events Being Tracked

The following custom events are automatically tracked:

| Event Name | Description | Parameters |
|------------|-------------|------------|
| `game_start` | New quiz round begins | `category`, `games_played` |
| `answer_submitted` | User answers a question | `correct`, `artist`, `category`, `total_correct`, `total_incorrect`, `accuracy_rate` |
| `perfect_score` | User gets 10/10 | `perfect_scores`, `category` |
| `category_changed` | User switches categories | `new_category`, `category_usage` |
| `session_end` | User leaves the site | `session_duration`, `total_correct`, `total_incorrect`, `games_played`, `perfect_scores` |

## 🔧 Using the Analytics Script

The `scripts/analytics.py` script helps you analyze your data:

```bash
# Show setup instructions
python scripts/analytics.py --setup

# View demo data (for testing)
python scripts/analytics.py --demo

# Export data as JSON
python scripts/analytics.py --export json

# Export data as CSV
python scripts/analytics.py --export csv
```

## 📈 Viewing Your Data

### Google Analytics Dashboard

1. **Real-Time Reports**: See live activity
2. **Events**: View custom event data
3. **Audience**: Demographics and location
4. **Acquisition**: How users find your site
5. **Behavior**: User engagement patterns

### Key Reports to Monitor

- **Events** → **All Events**: See all custom events
- **Audience** → **Geo** → **Location**: User locations
- **Audience** → **Technology**: Browser/device info
- **Behavior** → **Site Content**: Page views and time on site

## 🔒 Privacy Considerations

- Google Analytics respects user privacy settings
- Users can opt out via browser settings
- No personally identifiable information is collected
- Data is aggregated and anonymized

## 🚨 Troubleshooting

### No Data Appearing

1. **Check Measurement ID**: Ensure it's correctly set in `index.html`
2. **Wait 24-48 hours**: Data can take time to appear
3. **Check Real-Time**: Use Real-Time reports to see immediate data
4. **Browser Extensions**: Disable ad blockers temporarily for testing

### Events Not Tracking

1. **Check Console**: Look for JavaScript errors
2. **Verify gtag**: Ensure Google Analytics script loads
3. **Test Events**: Use browser dev tools to verify event firing

## 📱 Alternative Analytics Options

If you prefer privacy-focused alternatives:

### Simple Analytics
- Privacy-focused, GDPR compliant
- Very lightweight
- Free tier available

### Plausible Analytics
- Beautiful dashboards
- Privacy-focused
- $9/month for unlimited sites

### Self-Hosted Solutions
- Matomo (formerly Piwik)
- Open Web Analytics
- Requires server setup

## 🎯 Next Steps

1. **Set up Google Analytics** following the steps above
2. **Deploy your site** and wait for data to accumulate
3. **Run the analytics script** to view your metrics
4. **Monitor key metrics** like perfect scores and category usage
5. **Use insights** to improve your quiz content and user experience

## 📞 Support

If you need help with the analytics setup:

1. Check the Google Analytics help center
2. Verify your Measurement ID is correct
3. Test with the demo data first
4. Check browser console for errors

---

**Note**: Analytics data typically takes 24-48 hours to appear in Google Analytics reports, but Real-Time reports show data immediately. 