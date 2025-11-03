#!/usr/bin/env python3
"""
Create sample blog content for testing the RAG system
Run this if you don't have your markdown blog files ready yet
"""

import os
from pathlib import Path

# Sample blog content for BMX, fitness, and product knowledge
SAMPLE_BLOGS = [
    {
        "filename": "bmx-tricks-for-beginners.md",
        "content": """---
title: "Essential BMX Tricks Every Beginner Should Master"
category: "BMX Techniques"
tags: "bmx, tricks, beginner, tutorial"
date: "2024-01-15"
---

# Essential BMX Tricks Every Beginner Should Master

Starting your BMX journey can be overwhelming with all the tricks you see pros performing. Here are the fundamental tricks every beginner should focus on mastering first.

## 1. The Bunny Hop

The bunny hop is the foundation of almost every BMX trick. It's the ability to lift both wheels off the ground simultaneously without using a ramp.

**How to do it:**
- Start rolling at a comfortable speed
- Compress your body by bending your knees and elbows
- Pull up on the handlebars while pushing down with your feet
- As the front wheel comes up, push the bars forward and pull your knees to your chest
- Land with both wheels touching down at the same time

**Practice tips:**
- Start small - even a few inches counts
- Practice the motion while stationary first
- Focus on timing rather than height initially

## 2. Manual

A manual is riding on just your back wheel without pedaling. It's like a wheelie but requires different technique and balance.

**Key points:**
- Find your balance point through practice
- Use your body weight to control the front wheel
- Keep your arms straight and lean back
- Practice in a safe, open area

## 3. 180-Degree Turn

This trick involves turning your bike 180 degrees while in the air, landing facing the opposite direction.

**Steps:**
1. Approach with moderate speed
2. Bunny hop while turning your shoulders and hips
3. Spot your landing
4. Complete the rotation and prepare to ride backward or turn around

## Safety First

Always wear proper protective gear:
- Helmet (most important!)
- Knee and elbow pads
- Gloves for better grip
- Proper shoes with good grip

Remember, progression takes time. Master each trick completely before moving to the next level."""
    },
    {
        "filename": "cardio-training-for-bmx.md",
        "content": """---
title: "Cardio Training Essentials for BMX Riders"
category: "Fitness Training"
tags: "cardio, fitness, bmx, training, endurance"
date: "2024-01-20"
---

# Cardio Training Essentials for BMX Riders

BMX riding demands explosive power, but don't underestimate the importance of cardiovascular fitness. Whether you're racing or hitting the skate park, good cardio will improve your performance and recovery.

## Why Cardio Matters for BMX

BMX might seem like it's all about short bursts of power, but cardiovascular fitness plays several crucial roles:

- **Faster recovery** between runs or tricks
- **Better endurance** during long sessions
- **Improved focus** when you're not gasping for air
- **Injury prevention** through better overall fitness

## Best Cardio Exercises for BMX Riders

### 1. High-Intensity Interval Training (HIIT)

HIIT perfectly mimics the stop-and-go nature of BMX riding.

**Sample HIIT workout:**
- 30 seconds all-out effort
- 90 seconds active recovery
- Repeat 8-12 rounds

**Exercises to use:**
- Burpees
- Mountain climbers
- Jump squats
- Sprint intervals

### 2. Cycling-Specific Cardio

Nothing beats time on the bike for sport-specific fitness.

**Training methods:**
- Long, steady rides (45-90 minutes)
- Hill repeats
- Sprint intervals on flat ground
- Pump track sessions

### 3. Plyometric Training

Explosive movements that build power and cardio simultaneously.

**Key exercises:**
- Box jumps
- Broad jumps
- Lateral bounds
- Depth jumps

## Sample Weekly Cardio Plan

**Monday:** HIIT workout (20-30 minutes)
**Tuesday:** Easy bike ride (45-60 minutes)
**Wednesday:** Plyometric circuit (30 minutes)
**Thursday:** Rest or light activity
**Friday:** Sprint intervals (30 minutes)
**Saturday:** Long ride or BMX session
**Sunday:** Active recovery (walking, stretching)

## Monitoring Your Progress

Track these metrics to ensure you're improving:
- Resting heart rate (should decrease over time)
- Recovery heart rate (how quickly you recover after intense effort)
- Session duration (ability to maintain intensity longer)
- Perceived exertion (activities should feel easier over time)

## Nutrition for Cardio Training

Proper nutrition supports your cardio training:

**Before training:**
- Light carbohydrates 30-60 minutes before
- Avoid heavy meals 2-3 hours before intense sessions

**During training:**
- Water for sessions under 60 minutes
- Sports drinks for longer sessions

**After training:**
- Protein and carbohydrates within 30 minutes
- Focus on recovery foods like chocolate milk, bananas, or recovery shakes

Remember, consistency beats intensity. It's better to do moderate cardio regularly than intense sessions sporadically."""
    },
    {
        "filename": "choosing-the-right-bmx-bike.md",
        "content": """---
title: "How to Choose the Right BMX Bike: A Complete Buyer's Guide"
category: "Product Reviews"
tags: "bmx, bike, buying guide, equipment, review"
date: "2024-01-25"
---

# How to Choose the Right BMX Bike: A Complete Buyer's Guide

Choosing your first BMX bike (or upgrading your current one) can be overwhelming with so many options available. This guide will help you make an informed decision based on your riding style, budget, and goals.

## Types of BMX Bikes

### 1. Race BMX Bikes

Designed for BMX racing on tracks with jumps and berms.

**Characteristics:**
- Lightweight aluminum or carbon frames
- Larger wheels (20" with narrow tires)
- Longer wheelbase for stability at speed
- Single gear ratio optimized for acceleration
- Minimal brakes (rear only, sometimes none)

**Best for:** Competitive racing, speed-focused riding

### 2. Freestyle BMX Bikes

Built for tricks, stunts, and park riding.

**Characteristics:**
- Stronger, heavier frames (usually steel)
- Shorter wheelbase for maneuverability
- Front and rear brakes (or no brakes for advanced riders)
- Pegs for grinding
- More durable components

**Best for:** Skate parks, street riding, tricks

### 3. Dirt Jump BMX Bikes

Specialized for jumping and dirt track riding.

**Characteristics:**
- Medium weight between race and freestyle
- Strong frame with good shock absorption
- Knobby tires for traction
- Usually rear brake only
- Geometry optimized for jumping

**Best for:** Dirt jumps, trails, outdoor riding

## Key Components to Consider

### Frame Material

**Steel:**
- Pros: Durable, repairable, good feel
- Cons: Heavier than aluminum
- Best for: Freestyle, beginners, budget builds

**Aluminum:**
- Pros: Lightweight, corrosion-resistant
- Cons: Can be harsh, harder to repair
- Best for: Racing, weight-conscious riders

**Chromoly (Chrome Molybdenum Steel):**
- Pros: Strong, lightweight, good ride quality
- Cons: More expensive than regular steel
- Best for: High-end builds, serious riders

### Wheel Size

**20-inch wheels:** Standard for most BMX bikes
**24-inch wheels:** "Cruiser" BMX, easier for taller riders
**26-inch wheels:** Less common, for very tall riders

### Gearing

**Single Speed:** Most common, simple and reliable
**Multi-Speed:** Rare in BMX, mainly on cruiser bikes

## Sizing Your BMX Bike

BMX bike sizing is different from regular bikes. Consider:

### Top Tube Length
This is the most important measurement:
- **19.5-20.5":** Shorter riders (under 5'6")
- **20.5-21":** Average height riders (5'6" to 6')
- **21-21.5":** Taller riders (over 6')

### Standover Height
You should have 1-2 inches of clearance when standing over the bike.

## Budget Considerations

### Entry Level ($200-400)
- Basic steel frame
- Standard components
- Good for learning and casual riding
- Examples: Mongoose Legion, Haro Downtown

### Mid-Range ($400-800)
- Better frame materials (chromoly)
- Improved components
- More durable for regular use
- Examples: Fit Bike Co. Series One, Kink Gap

### High-End ($800+)
- Premium materials and components
- Lightweight and durable
- Professional-level performance
- Examples: Sunday Blueprint, Cult Devotion

## What to Look for When Buying

### New Bikes
- Warranty coverage
- Proper assembly from bike shop
- Latest technology and standards
- Full component compatibility

### Used Bikes
- Check frame for cracks or damage
- Inspect wheels for true and spoke tension
- Test brakes and shifting (if applicable)
- Verify all components are secure

## Essential Accessories

Don't forget these important additions:

**Safety Gear:**
- Helmet (most important!)
- Knee and elbow pads
- Gloves

**Maintenance Tools:**
- Multi-tool with hex keys
- Tire pump
- Chain lube
- Basic repair kit

**Optional Upgrades:**
- Pegs for grinding
- Different pedals for better grip
- Upgraded grips
- Chain guard

## Final Tips

1. **Test ride** if possible - feel is important
2. **Buy from reputable dealers** for warranty and support
3. **Consider your local riding spots** - what type of riding will you do most?
4. **Don't overspend initially** - you can always upgrade later
5. **Prioritize safety gear** in your budget

Remember, the best BMX bike is the one that fits your riding style, budget, and gets you excited to ride. Start with something appropriate for your skill level and upgrade as your skills and interests develop."""
    },
    {
        "filename": "bmx-bike-maintenance-guide.md",
        "content": """---
title: "Essential BMX Bike Maintenance: Keep Your Ride Running Smooth"
category: "Maintenance"
tags: "maintenance, bmx, bike care, repair, tools"
date: "2024-02-01"
---

# Essential BMX Bike Maintenance: Keep Your Ride Running Smooth

Regular maintenance keeps your BMX bike performing at its best and extends its lifespan. Here's everything you need to know about keeping your ride in top condition.

## Daily Pre-Ride Checks

Before every session, do a quick safety check:

### The ABC Quick Check
- **A**ir: Check tire pressure and look for damage
- **B**rakes: Test brake function and pad wear
- **C**rank: Ensure pedals and cranks are tight

### Additional Quick Checks
- Wheel quick-releases or bolts tight
- Handlebars aligned and secure
- Chain properly lubricated
- No unusual noises when spinning wheels

## Weekly Maintenance Tasks

### Chain Care
**Cleaning:**
1. Use degreaser or chain cleaning tool
2. Scrub with old toothbrush if heavily soiled
3. Rinse with water (avoid high pressure on bearings)
4. Dry completely

**Lubrication:**
1. Apply chain lube to inside of chain while pedaling backward
2. Wipe excess lube with clean rag
3. Let sit for a few minutes before riding

### Tire Inspection
- Check for embedded debris (glass, thorns)
- Look for cuts or excessive wear
- Ensure proper tire pressure (usually 40-65 PSI for BMX)
- Inspect sidewalls for damage

### Brake Adjustment
**For rim brakes:**
- Check pad alignment with rim
- Adjust cable tension if needed
- Replace pads when worn down

**For disc brakes:**
- Check rotor for warping or damage
- Ensure pads have adequate material
- Test lever feel and adjust as needed

## Monthly Deep Maintenance

### Drivetrain Deep Clean
1. Remove chain for thorough cleaning
2. Clean chainring and rear cog/cassette
3. Inspect chain for wear using chain checker tool
4. Replace chain if stretched beyond 0.5% (11-speed) or 0.75% (single speed)

### Wheel Maintenance
**Spoke Tension:**
- Check for loose or broken spokes
- True wheels if they wobble side-to-side
- Consider professional wheel building if multiple spokes are loose

**Hub Service:**
- Check for play in wheel bearings
- Repack bearings with grease annually
- Replace bearings if rough or damaged

### Headset Service
1. Check for play by holding front brake and rocking bike
2. Adjust preload if loose
3. Regrease bearings annually
4. Replace if rough or damaged

## Seasonal Maintenance

### Spring Tune-Up
- Complete bike wash and inspection
- Replace cables and housing
- Service all bearings (headset, bottom bracket, hubs)
- Check frame for cracks or damage
- Replace worn components

### Winter Storage (if applicable)
- Clean and lubricate entire bike
- Store in dry location
- Consider removing wheels to prevent flat spots
- Check tire pressure monthly during storage

## Essential Tools for BMX Maintenance

### Basic Tool Kit
- Multi-tool with hex keys (4, 5, 6, 8mm most common)
- Chain tool
- Tire levers
- Pump with pressure gauge
- Chain lube
- Degreaser
- Clean rags

### Advanced Tools
- Torque wrench
- Chain checker
- Spoke wrench
- Bottom bracket tools
- Headset tools
- Cable cutters

## Common Problems and Solutions

### Chain Skipping
**Causes:** Worn chain, worn cog, poor adjustment
**Solutions:** Replace chain, adjust derailleur, replace worn components

### Squeaky Brakes
**Causes:** Dirty rims, glazed pads, poor alignment
**Solutions:** Clean rims, sand brake pads, adjust alignment

### Wobbly Wheel
**Causes:** Loose spokes, damaged rim, hub issues
**Solutions:** True wheel, tighten spokes, replace damaged parts

### Creaking Noises
**Causes:** Dry bearings, loose components, frame issues
**Solutions:** Lubricate bearings, check all bolts, inspect frame

## When to Seek Professional Help

Consider taking your bike to a shop for:
- Wheel building or major truing
- Bottom bracket service
- Headset replacement
- Frame damage assessment
- Complex brake or shifting issues

## Maintenance Schedule Summary

**Before every ride:** ABC check
**Weekly:** Chain care, tire inspection, brake check
**Monthly:** Deep clean, wheel check, headset check
**Seasonally:** Complete service, bearing maintenance
**Annually:** Replace cables, comprehensive inspection

## Pro Tips

1. **Keep it simple:** BMX bikes are relatively simple - don't overthink maintenance
2. **Quality tools matter:** Invest in good basic tools that will last
3. **Learn gradually:** Start with basic maintenance and build skills over time
4. **Document issues:** Keep track of when you replace components
5. **Prevention is key:** Regular small maintenance prevents big problems

Remember, a well-maintained BMX bike is safer, performs better, and lasts longer. Start with the basics and gradually build your maintenance skills as you become more comfortable working on your bike."""
    }
]

def create_sample_blogs(output_dir="sample_blogs"):
    """Create sample blog markdown files."""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"Creating sample blog files in {output_dir}/")
    
    for blog in SAMPLE_BLOGS:
        file_path = Path(output_dir) / blog["filename"]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(blog["content"])
        
        print(f"✅ Created: {blog['filename']}")
    
    print(f"\n🎉 Created {len(SAMPLE_BLOGS)} sample blog files!")
    print(f"📁 Location: {Path(output_dir).absolute()}")
    print("\nNext steps:")
    print(f"1. Run: python convert_md_to_json.py {output_dir} -r")
    print("2. This will create processed_blogs.json for your RAG system")

if __name__ == "__main__":
    create_sample_blogs()