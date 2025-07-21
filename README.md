# Smart Requirements Upgrader 🚀

A Python tool that intelligently upgrades your `requirements.txt` file while maintaining package compatibility. Unlike simple version upgraders that break dependencies, this tool uses pip's actual dependency resolver to ensure your packages work together.

## 🎯 Features

- **Smart Compatibility Checking**: Uses pip's built-in dependency resolver
- **Progressive Fix Strategies**: Tries multiple approaches until one works
- **Known Conflict Resolution**: Automatically fixes common ML/Flask package conflicts
- **Flexible Version Ranges**: Creates maintainable requirements with version ranges
- **User-Friendly GUI**: Simple point-and-click interface
- **Template Generation**: Provides battle-tested ML/Flask starter templates

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/auto-requirements-upgrader.git
cd auto-requirements-upgrader
```

2. Install dependencies:
```bash
pip install tkinter  # Usually included with Python
```

3. Run the script:
```bash
python auto-up-smart-compatibility.py
```

## 🚀 Usage

### Option 1: Fix Existing Requirements File
1. Run the script
2. Choose "YES" when prompted
3. Select your `requirements.txt` file
4. The tool will:
   - Test your current requirements
   - Apply smart fixes for known conflicts
   - Generate a compatible version with flexible ranges
   - Save the result as `requirements-compatible.txt`

### Option 2: Create ML Template (Recommended for New Projects)
1. Run the script
2. Choose "NO" when prompted
3. Choose where to save the template
4. Get a pre-configured, compatible ML stack including:
   - Flask web framework
   - OpenCV for computer vision
   - PyTorch for ML
   - AWS SDK (boto3)
   - Testing frameworks
   - Production server (gunicorn)

## 🧠 How It Works

The tool uses a **progressive strategy approach**:

1. **Original Test**: Tests your current requirements as-is
2. **Known Fixes**: Applies fixes for common conflicts like:
   - `numpy>=2.0.0,<2.3.0` (OpenCV compatibility)
   - More conservative Pillow/SciPy versions
3. **Flexible Versions**: Converts exact pins (`==1.2.3`) to ranges (`>=1.2.0`)
4. **Combined Approach**: Uses both fixes and flexibility

Each strategy is tested using `pip install --dry-run` to ensure it actually works.

## 📊 Example Transformations

### Before (Broken):
```
numpy==2.3.1
opencv-python==4.12.0.88
pillow==11.3.0
```

### After (Compatible):
```
numpy>=2.0.0,<2.3.0  # OpenCV compatibility fix
opencv-python>=4.12.0
pillow>=10.0.0       # More compatible base version
```

## 🎯 Common Fixes Applied

| Issue | Solution | Reason |
|-------|----------|---------|
| `numpy==2.3.1` | `numpy>=2.0.0,<2.3.0` | OpenCV requires numpy < 2.3.0 |
| `pillow>=11.3.0` | `pillow>=10.0.0` | Broader compatibility |
| `scipy>=1.16.0` | `scipy>=1.11.0` | More stable base version |
| Exact pins | Flexible ranges | Allows security updates |

## 📁 File Structure

```
auto-requirements-upgrader/
├── auto-up-smart-compatibility.py  # Main smart upgrader
├── auto-up.py                     # Simple version upgrader
├── README.md                      # This file
└── requirements_files/
    ├── requirements.txt           # Original requirements
    ├── requirements-upgraded.txt  # Latest versions (may break)
    └── requirements-compatible.txt # Smart fixed versions
```

## 🆚 Comparison with Simple Upgrader

| Feature | Simple Upgrader | Smart Upgrader |
|---------|----------------|----------------|
| Speed | Fast ⚡ | Moderate 🐢 |
| Compatibility | Often breaks 💥 | Guaranteed ✅ |
| Conflict Resolution | None ❌ | Automatic 🤖 |
| Version Strategy | Latest exact pins | Flexible ranges |
| Use Case | Quick updates | Production ready |

## 🔍 Debugging Failed Upgrades

If the tool can't fix your requirements:

1. **Check the output** - Look for specific conflict details
2. **Manual review** - Some conflicts need human judgment
3. **Incremental approach** - Try upgrading packages one by one
4. **Version constraints** - Some packages may need older versions

Common conflict patterns:
```
ERROR: package-a 2.0.0 depends on package-b<1.5.0
       package-c 3.0.0 depends on package-b>=1.6.0
```

## 🎯 Best Practices

### For Development:
- Use the Smart Upgrader for dependency resolution
- Test your application after upgrading
- Keep a backup of working requirements

### For Production:
- Use flexible ranges (`>=1.2.0`) over exact pins (`==1.2.3`)
- Pin only when necessary (known breaking changes)
- Regular security updates with `pip install --upgrade`

### For ML Projects:
- Start with the provided ML template
- Be cautious with CUDA versions for GPU workloads
- Test model compatibility after upgrades

## 🚨 Known Limitations

- **Timeout**: Complex dependency trees may take 60+ seconds
- **CUDA Packages**: GPU-specific packages need manual attention  
- **Development Dependencies**: May be more conservative than needed
- **Platform Specific**: Some packages have different requirements on Windows/Linux/Mac

## 🛠️ Troubleshooting

### "All strategies failed"
- Try the ML template instead
- Manually remove problematic packages
- Check for platform-specific issues

### "Timeout during testing"
- Reduce number of packages
- Check internet connection
- Try again (sometimes pip registry is slow)

### GUI not working
- Ensure tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt install python3-tk`
- Run from command line to see error messages

## 📈 Example Success Story

**Before**: 18 packages with dependency conflicts
```
❌ Original requirements have conflicts
ERROR: Cannot install opencv-python==4.12.0.88 and numpy==2.3.1 
because these package versions have conflicting dependencies.
```

**After**: Using "Fixed conflicts" strategy
```
✅ Fixed conflicts - SUCCESS!
💾 Compatible requirements saved to: requirements-compatible.txt

📝 Changes made:
  numpy==2.3.1 → numpy>=2.0.0,<2.3.0
  pillow==11.3.0 → pillow>=10.0.0
  scipy==1.16.0 → scipy>=1.11.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with various requirements files
5. Submit a pull request

### Ideas for Contributions:
- More conflict resolution rules
- Platform-specific handling
- CLI interface
- Integration with poetry/pipenv
- Automated testing

## 📜 License

MIT License - See LICENSE file for details

## 🙋‍♂️ FAQ

**Q: Why not just use `pip install --upgrade`?**
A: That upgrades packages individually and often creates conflicts. This tool ensures the entire set works together.

**Q: Should I use exact versions or ranges?**
A: Ranges are better for maintenance - you get security updates automatically. Use exact pins only for known problematic packages.

**Q: Will this work with my custom packages?**
A: Yes! The tool works with any pip-installable package, including private repositories and custom indexes.

**Q: Can I add my own conflict fixes?**
A: Absolutely! Edit the `conflict_fixes` dictionary in `fix_dependency_conflicts()` function.

---

Made with ❤️ for Python developers who want their dependencies to actually work together!
