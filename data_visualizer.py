import matplotlib.pyplot as plt
import pandas as pd

def generate_chart(df, title="Business Data Insights"):
    """
    Generates a high-contrast, premium light-themed Dashboard Card 
    inspired by top-tier modern infographics.
    """
    if df is None or df.empty:
        print("⚠️ No data available to visualize.")
        return False

    cols = df.columns
    if len(cols) == 2:
        col1_type = df[cols[0]].dtype
        col2_type = df[cols[1]].dtype
        
        x_col, y_col = None, None
        
        if pd.api.types.is_numeric_dtype(col2_type):
            x_col, y_col = cols[0], cols[1]
        elif pd.api.types.is_numeric_dtype(col1_type):
            x_col, y_col = cols[1], cols[0]
            
        if x_col and y_col:
            # 1. Start with an ultra-clean white card style
            fig, ax = plt.subplots(figsize=(9.5, 6), facecolor='#FFFFFF') # Solid white card backdrop
            ax.set_facecolor('#FFFFFF') # Internal card area is also white
            
            # 2. Extracting premium warmth from Image 8: Vivid orange-red, bright gold, corporate cyan
            premium_colors = ['#D9463E', '#FFBF00', '#00A8E8', '#FF6B35', '#2A9D8F']
            
            # Dynamic colors for the dataset size
            num_bars = len(df)
            bar_colors = [premium_colors[i % len(premium_colors)] for i in range(num_bars)]
            
            # 3. Draw clean, solid-fill bars (No glow, nice flat corporate borders)
            bars = ax.bar(df[x_col].astype(str), df[y_col], 
                          color=bar_colors, width=0.5, alpha=0.95, 
                          edgecolor=[c for c in bar_colors], linewidth=1)
            
            # 4. Bold data labels right on top of the bars with deep charcoal contrast
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.015), 
                        f'{yval:g}', ha='center', va='bottom', 
                        fontsize=12, fontweight='bold', color='#2B2D42') # Slate dark grey
            
            # 5. Clean, high-legibility axis and title text
            ax.set_xlabel(x_col.upper(), fontsize=10, fontweight='bold', color='#6C757D', labelpad=12)
            ax.set_ylabel(y_col.upper(), fontsize=10, fontweight='bold', color='#6C757D', labelpad=12)
            
            # Left-aligned prominent headline inspired by infographic titles
            ax.set_title(title, fontsize=15, fontweight='bold', color='#1A1D20', pad=25, loc='left')
            
            # 6. Completely remove borders (Spines) for edge-less visual elegance
            for spine in ['top', 'right', 'left']:
                ax.spines[spine].set_visible(False)
            ax.spines['bottom'].set_color('#DEE2E6') # Very faint border at bottom
            
            # 7. Subtle horizontal guide lines (Light grey)
            ax.yaxis.grid(True, linestyle='--', alpha=0.6, color='#E9ECEF')
            ax.xaxis.grid(False)
            
            # Clear ticks that integrate perfectly
            ax.tick_params(axis='x', colors='#495057', labelsize=11)
            ax.tick_params(axis='y', left=False, labelleft=False) # Hide Y axis numbers as bar values are directly printed
            
            # Auto adjustment
            plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9)
            plt.tight_layout()
            
            # 8. Save at 300 DPI (High Resolution)
            filename = "latest_chart.png"
            plt.savefig(filename, dpi=300, facecolor='#FFFFFF', edgecolor='none', bbox_inches='tight')
            plt.close()
            
            print(f"📈 Premium Light-Theme Chart successfully generated and saved as '{filename}'")
            return True

    print("ℹ️ Data format is not suitable for this custom chart.")
    return False

if __name__ == "__main__":
    data = {'Category': ['Furniture', 'Electronics', 'Appliances'], 'Quantity': [19, 10, 6]}
    test_df = pd.DataFrame(data)
    print("📊 Testing Premium light visualizer...")
    generate_chart(test_df, "Show total quantity ordered for each product category.")