# Wikimedia Commons Category Strategy Guide

## 🎯 **The Problem: Hierarchical Categories**

Wikimedia Commons uses a hierarchical category structure where main categories often contain subcategories rather than direct files. For example:

```
Category:Paintings by Christian Krohg by museum
├── Paintings by Christian Krohg in Göteborgs Konstmuseum (4 F)
├── Paintings by Christian Krohg in KODE Art Museums (8 F)
├── Paintings by Christian Krohg in Lillehammer kunstmuseum (7 F)
└── Paintings by Christian Krohg in the Nasjonalmuseet (83 F)
```

## 🚀 **Solution: Smart Subcategory Handling**

The enhanced `collect_art.py` script now automatically:

### **1. Detects Subcategories**
- Scans category pages for subcategory links
- Identifies museum-specific and location-specific subcategories
- Skips administrative categories (Good pictures, Featured pictures, etc.)

### **2. Fetches from Subcategories**
- Automatically follows subcategory links
- Collects images from all relevant subcategories
- Respects the `--max` limit across all subcategories combined

### **3. Avoids Duplicates**
- Removes duplicate URLs automatically
- Prevents the same image from being collected multiple times

## 📋 **Usage Strategies**

### **Strategy 1: Use Main Categories (Recommended)**
```bash
# This will automatically fetch from all subcategories
python collect_art.py --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_by_museum"
```

**Pros:**
- ✅ Gets ALL paintings from all museums
- ✅ No duplicates
- ✅ Single command
- ✅ Respects max limits

**Cons:**
- ⚠️ May take longer to process
- ⚠️ More verbose output

### **Strategy 2: Use Specific Subcategories**
```bash
# Target specific museums only
python collect_art.py --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_in_the_Nasjonalmuseet"
```

**Pros:**
- ✅ Faster processing
- ✅ More control over which museums
- ✅ Less verbose output

**Cons:**
- ❌ Need to manually identify subcategories
- ❌ Risk of missing paintings from other museums

### **Strategy 3: Disable Subcategories**
```bash
# Only fetch from main category (usually empty)
python collect_art.py --url "https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_by_museum" --no-subcategories
```

**Use when:**
- Main category actually contains files
- You want to avoid subcategory processing
- Testing purposes

## 🎨 **Recommended URL Strategy**

### **For Maximum Coverage:**
Use main category URLs like:
- `Category:Paintings_by_[Artist]_by_museum`
- `Category:Paintings_by_[Artist]`
- `Category:Artworks_by_[Artist]`

### **For Specific Collections:**
Use museum-specific URLs like:
- `Category:Paintings_by_[Artist]_in_[Museum]`
- `Category:Paintings_by_[Artist]_in_the_Nasjonalmuseet`

## 🔧 **Updated URLs.txt Strategy**

Consider updating your `urls.txt` to use main categories:

```txt
# Christian Krohg - Use main category for maximum coverage
https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_by_museum

# Or use specific museums if you prefer
https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_in_the_Nasjonalmuseet
https://commons.wikimedia.org/wiki/Category:Paintings_by_Christian_Krohg_in_KODE_Art_Museums
```

## 📊 **Performance Tips**

1. **Start with main categories** for comprehensive collection
2. **Use `--max`** to control collection size
3. **Use `--quiet`** to reduce output verbosity
4. **Monitor with `--diagnose`** to track collection health

## 🎯 **Best Practice Workflow**

1. **Test with dry run:**
   ```bash
   python collect_art.py --url "main_category_url" --max 10 --dry-run
   ```

2. **Collect with limits:**
   ```bash
   python collect_art.py --url "main_category_url" --max 100 --quiet
   ```

3. **Monitor collection:**
   ```bash
   python diagnostics.py
   ```

This approach ensures you get the most comprehensive collection while avoiding duplicates and maintaining control over the process! 🎨✨ 