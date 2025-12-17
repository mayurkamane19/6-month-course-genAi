import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

df = pd.read_csv(r"C:\Users\mayur\Downloads\archive (7)\student_performance.csv")

print(f"Dataset shape: {df.shape}")
print(f"\nColumn names: {list(df.columns)}")
print(f"\nFirst few rows:")
df.head()

print("Data Overview:")
print(df.info())
print("\n" + "="*50)
print("\nSummary Statistics:")
print(df.describe())
print("\n" + "="*50)
print("\nMissing Values:")
print(df.isnull().sum())

# Study Time vs Total Score - Simple, Clean Visualization
plt.clf()  # Clear any previous plots
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate correlation and R²
correlation = df['weekly_self_study_hours'].corr(df['total_score'])
z = np.polyfit(df['weekly_self_study_hours'], df['total_score'], 1)
p = np.poly1d(z)
r_squared = correlation ** 2

# Simple scatterplot with subtle color
ax.scatter(
    df['weekly_self_study_hours'], 
    df['total_score'],
    alpha=0.15,
    s=15,
    c='#4A90E2',  # Soft blue
    edgecolors='none'
)

# Subtle trend line
ax.plot(df['weekly_self_study_hours'], p(df['weekly_self_study_hours']), 
        linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)

# Simple annotation in corner
stats_text = f'r = {correlation:.2f}  |  R² = {r_squared:.2f}'
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, 
        fontsize=10, horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='none'))

# Clean, minimal styling
ax.set_xlabel('Weekly Self-Study Hours', fontsize=12, color='#333333', labelpad=8)
ax.set_ylabel('Total Score', fontsize=12, color='#333333', labelpad=8)
ax.set_title('Study Time and Academic Performance', 
             fontsize=16, fontweight='600', pad=15, color='#2C3E50')

# Minimal spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E0E0E0')
ax.spines['bottom'].set_color('#E0E0E0')

# Subtle grid
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax.set_axisbelow(True)

# Set y-axis limits
y_min = df['total_score'].min()
y_max = df['total_score'].max()
ax.set_ylim(y_min - 2, y_max + 2)

plt.tight_layout()
plt.show()

print(f"Correlation: {correlation:.3f} | R²: {r_squared:.3f} | Slope: {z[0]:.2f} points per hour")

# Attendance vs Total Score - Simple, Clean Visualization
plt.clf()  # Clear any previous plots
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate correlation and R²
correlation = df['attendance_percentage'].corr(df['total_score'])
z = np.polyfit(df['attendance_percentage'], df['total_score'], 1)
p = np.poly1d(z)
r_squared = correlation ** 2

# Simple scatterplot with subtle color
ax.scatter(
    df['attendance_percentage'], 
    df['total_score'],
    alpha=0.15,
    s=15,
    c='#7ED321',  # Soft green
    edgecolors='none'
)

# Subtle trend line
ax.plot(df['attendance_percentage'], p(df['attendance_percentage']), 
        linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)

# Simple annotation in corner
stats_text = f'r = {correlation:.2f}  |  R² = {r_squared:.2f}'
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, 
        fontsize=10, horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='none'))

# Clean, minimal styling
ax.set_xlabel('Attendance Percentage (%)', fontsize=12, color='#333333', labelpad=8)
ax.set_ylabel('Total Score', fontsize=12, color='#333333', labelpad=8)
ax.set_title('Attendance and Academic Performance', 
             fontsize=16, fontweight='600', pad=15, color='#2C3E50')

# Minimal spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E0E0E0')
ax.spines['bottom'].set_color('#E0E0E0')

# Subtle grid
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax.set_axisbelow(True)

# Set y-axis limits
y_min = df['total_score'].min()
y_max = df['total_score'].max()
ax.set_ylim(y_min - 2, y_max + 2)

plt.tight_layout()
plt.show()

print(f"Correlation: {correlation:.3f} | R²: {r_squared:.3f} | Slope: {z[0]:.2f} points per %")

# Class Participation vs Total Score - Simple, Clean Visualization
plt.clf()  # Clear any previous plots
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate correlation on original continuous variable
correlation = df['class_participation'].corr(df['total_score'])
z = np.polyfit(df['class_participation'], df['total_score'], 1)
p = np.poly1d(z)
r_squared = correlation ** 2

# Use scatterplot instead of boxplot to show actual relationship
ax.scatter(
    df['class_participation'], 
    df['total_score'],
    alpha=0.15,
    s=15,
    c='#9B59B6',  # Soft purple
    edgecolors='none'
)

# Subtle trend line
ax.plot(df['class_participation'], p(df['class_participation']), 
        linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)

# Simple annotation
stats_text = f'r = {correlation:.2f}  |  R² = {r_squared:.2f}'
ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, 
        fontsize=10, horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='none'))

# Clean, minimal styling
ax.set_xlabel('Class Participation Level', fontsize=12, color='#333333', labelpad=8)
ax.set_ylabel('Total Score', fontsize=12, color='#333333', labelpad=8)
ax.set_title('Participation and Academic Performance', 
             fontsize=16, fontweight='600', pad=15, color='#2C3E50')

# Set x-axis to show 0-10 range clearly
ax.set_xlim(-0.5, 10.5)
ax.set_xticks(range(0, 11))

# Set y-axis limits
y_min = df['total_score'].min()
y_max = df['total_score'].max()
ax.set_ylim(y_min - 2, y_max + 2)

# Minimal spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E0E0E0')
ax.spines['bottom'].set_color('#E0E0E0')

# Subtle grid
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()

print(f"Correlation: {correlation:.3f} | R²: {r_squared:.3f}")

# Reset any previous plot state
plt.clf()

fig = plt.figure(figsize=(16, 10))

# Calculate correlations
corr_study = df['weekly_self_study_hours'].corr(df['total_score'])
corr_attendance = df['attendance_percentage'].corr(df['total_score'])
corr_participation = df['class_participation'].corr(df['total_score'])

# Calculate consistent y-axis limits for ALL plots (use same limits everywhere)
y_min = df['total_score'].min()
y_max = df['total_score'].max()
y_buffer = 2
y_lim_low = y_min - y_buffer
y_lim_high = y_max + y_buffer

ax1 = plt.subplot(2, 2, 1)
z1 = np.polyfit(df['weekly_self_study_hours'], df['total_score'], 1)
p1 = np.poly1d(z1)
ax1.scatter(df['weekly_self_study_hours'], df['total_score'], 
           alpha=0.12, s=12, c='#4A90E2', edgecolors='none')
ax1.plot(df['weekly_self_study_hours'], p1(df['weekly_self_study_hours']), 
         linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)
ax1.set_xlabel('Weekly Study Hours', fontsize=10, color='#333333')
ax1.set_ylabel('Total Score', fontsize=10, color='#333333')
ax1.set_ylim(y_lim_low, y_lim_high)
ax1.set_title(f'Study Time (r = {corr_study:.2f})', fontsize=12, fontweight='600', pad=8, color='#2C3E50')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#E0E0E0')
ax1.spines['bottom'].set_color('#E0E0E0')
ax1.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax1.set_axisbelow(True)

# Top right: Attendance
ax2 = plt.subplot(2, 2, 2)
z2 = np.polyfit(df['attendance_percentage'], df['total_score'], 1)
p2 = np.poly1d(z2)
ax2.scatter(df['attendance_percentage'], df['total_score'], 
           alpha=0.12, s=12, c='#7ED321', edgecolors='none')
ax2.plot(df['attendance_percentage'], p2(df['attendance_percentage']), 
         linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)
ax2.set_xlabel('Attendance %', fontsize=10, color='#333333')
ax2.set_ylabel('Total Score', fontsize=10, color='#333333')
ax2.set_ylim(y_lim_low, y_lim_high)
ax2.set_title(f'Attendance (r = {corr_attendance:.2f})', fontsize=12, fontweight='600', pad=8, color='#2C3E50')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#E0E0E0')
ax2.spines['bottom'].set_color('#E0E0E0')
ax2.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax2.set_axisbelow(True)

# Bottom left: Participation
ax3 = plt.subplot(2, 2, 3)
z3 = np.polyfit(df['class_participation'], df['total_score'], 1)
p3 = np.poly1d(z3)
ax3.scatter(df['class_participation'], df['total_score'], 
           alpha=0.12, s=12, c='#9B59B6', edgecolors='none')
ax3.plot(df['class_participation'], p3(df['class_participation']), 
         linestyle='-', linewidth=2, color='#2C3E50', alpha=0.8)
ax3.set_xlabel('Participation Level', fontsize=10, color='#333333')
ax3.set_ylabel('Total Score', fontsize=10, color='#333333')
ax3.set_xlim(-0.5, 10.5)
ax3.set_xticks(range(0, 11))
ax3.set_ylim(y_lim_low, y_lim_high)
ax3.set_title(f'Participation (r = {corr_participation:.2f})', fontsize=12, fontweight='600', pad=8, color='#2C3E50')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#E0E0E0')
ax3.spines['bottom'].set_color('#E0E0E0')
ax3.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, color='#E0E0E0')
ax3.set_axisbelow(True)

# Bottom right: Combined Performance by Factor Levels
ax4 = plt.subplot(2, 2, 4)
# Create categories for each factor (use copy to avoid modifying original df)
df_dash = df.copy()
df_dash['study_category'] = pd.cut(df_dash['weekly_self_study_hours'], 
                                    bins=[0, 10, 15, 20, 100], 
                                    labels=['Low (0-10h)', 'Medium (10-15h)', 'High (15-20h)', 'Very High (20h+)'])
df_dash['attendance_category'] = pd.cut(df_dash['attendance_percentage'], 
                                         bins=[0, 75, 85, 95, 100], 
                                         labels=['Low (<75%)', 'Medium ((75-85%)', 'High (85-95%)', 'Very High (95%+)'])
df_dash['participation_category'] = pd.cut(df_dash['class_participation'], 
                                           bins=[0, 4, 6, 8, 10], 
                                           labels=['Low (0-4)', 'Medium (4-6)', 'High (6-8)', 'Very High (8+)'])

# Calculate average scores by combination
combined = df_dash.groupby(['study_category', 'attendance_category', 'participation_category'], observed=True)['total_score'].mean().reset_index()
combined = combined.sort_values('total_score', ascending=False)

# Show top and bottom combinations
top_bottom = pd.concat([combined.head(5), combined.tail(5)])
colors_combo = ['#4A90E2' if i < 5 else '#BDC3C7' for i in range(len(top_bottom))]
bars = ax4.barh(range(len(top_bottom)), top_bottom['total_score'], color=colors_combo, alpha=0.6, edgecolor='#2C3E50', linewidth=0.5)

ax4.set_yticks(range(len(top_bottom)))
ax4.set_yticklabels([f"{row['study_category'][:4]}/{row['attendance_category'][:4]}/{row['participation_category'][:4]}" 
                     for _, row in top_bottom.iterrows()], fontsize=8, color='#333333')
ax4.set_xlabel('Average Total Score', fontsize=10, color='#333333')
ax4.set_title('Factor Combinations\n(Top 5 & Bottom 5)', fontsize=12, fontweight='600', pad=8, color='#2C3E50')
ax4.set_xlim(0, 100)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_color('#E0E0E0')
ax4.spines['bottom'].set_color('#E0E0E0')
ax4.grid(True, alpha=0.15, linestyle='-', linewidth=0.5, axis='x', color='#E0E0E0')
ax4.set_axisbelow(True)

plt.suptitle('Student Performance Dashboard', 
             fontsize=16, fontweight='600', y=0.98, color='#2C3E50')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

print(f"\nKey Insight: Top factor combinations average {combined.head(5)['total_score'].mean():.1f} points.")
print(f"Bottom factor combinations average {combined.tail(5)['total_score'].mean():.1f} points.")
print(f"That's a {combined.head(5)['total_score'].mean() - combined.tail(5)['total_score'].mean():.1f}-point difference.")
