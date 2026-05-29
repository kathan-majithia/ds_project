import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data(df):

    stats = {}
    print("\nBASIC STATISTICS")
    print(f"Total transactions: {len(df)}")
    print(f"Date range: {df['DateTime'].min()} to {df['DateTime'].max()}")
    print(f"Avg transaction: {df['total_value'].mean():.2f} ETH")
    print(f"Max transaction: {df['total_value'].max():.2f} ETH")
    stats['avg_tx'] = df['total_value'].mean()
    
    print(f"\nWHALE TRANSACTIONS")
    whale_txs = df[df['is_whale'] == 1]
    print(f"Whale txs: {len(whale_txs)} ({len(whale_txs)/len(df)*100:.1f}%)")
    print(f"Whale avg value: {whale_txs['total_value'].mean():.2f} ETH")
    stats['whale_count'] = len(whale_txs)
    
    print(f"\n⏰ TIME PATTERNS")
    peak_hour = df.groupby('hour')['total_value'].sum().idxmax()
    print(f"Peak activity hour: {peak_hour}:00 UTC")
    stats['peak_hour'] = peak_hour
    
    peak_day = df.groupby('day_of_week')['total_value'].sum().idxmax()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    print(f"Peak activity day: {days[peak_day]}")
    stats['peak_day'] = days[peak_day]
    
    print(f"\n💰 FEE ANALYSIS")
    print(f"Avg fee: {df['TxnFee(ETH)'].mean():.6f} ETH")
    print(f"Fee correlation with size: {df['total_value'].corr(df['TxnFee(ETH)']):.3f}")
    stats['fee_correlation'] = df['total_value'].corr(df['TxnFee(ETH)'])
    
    print(f"\n⚠️ OUTLIERS")
    Q3 = df['total_value'].quantile(0.75)
    IQR = Q3 - df['total_value'].quantile(0.25)
    outliers = df[df['total_value'] > Q3 + 1.5*IQR]
    print(f"Outlier transactions: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")
    stats['outliers'] = len(outliers)
    
    return stats

def plot_insights(df):

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Ethereum Whale Transaction Analysis', fontsize=16, fontweight='bold')
    
    axes[0,0].hist(df['total_value'], bins=50, color='skyblue', edgecolor='black')
    axes[0,0].set_title('Transaction Value Distribution')
    axes[0,0].set_xlabel('Value (ETH)')
    axes[0,0].set_ylabel('Frequency')
    
    whale_data = [df[df['is_whale']==0]['total_value'], 
                  df[df['is_whale']==1]['total_value']]
    axes[0,1].boxplot(whale_data, labels=['Normal', 'Whale'])
    axes[0,1].set_title('Whale vs Normal Transactions')
    axes[0,1].set_ylabel('Value (ETH)')
    
    hourly = df.groupby('hour')['total_value'].sum()
    axes[0,2].bar(hourly.index, hourly.values, color='green', alpha=0.7)
    axes[0,2].set_title('Transaction Volume by Hour')
    axes[0,2].set_xlabel('Hour (UTC)')
    axes[0,2].set_ylabel('Total ETH')
    
    daily = df.groupby('day_of_week')['total_value'].sum()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    axes[1,0].bar(range(7), daily.values, color='orange', alpha=0.7)
    axes[1,0].set_xticks(range(7))
    axes[1,0].set_xticklabels(days)
    axes[1,0].set_title('Transaction Volume by Day')
    axes[1,0].set_ylabel('Total ETH')
    
    axes[1,1].scatter(df['total_value'], df['TxnFee(ETH)'], alpha=0.3, s=10)
    axes[1,1].set_title('Transaction Fee vs Size')
    axes[1,1].set_xlabel('Value (ETH)')
    axes[1,1].set_ylabel('Fee (ETH)')
    
    daily_tx = df.groupby('DateTime').size()
    axes[1,2].plot(daily_tx.index, daily_tx.values, color='red', linewidth=1)
    axes[1,2].set_title('Transaction Count Over Time')
    axes[1,2].set_xlabel('Date')
    axes[1,2].set_ylabel('Count')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('ethereum_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: ethereum_analysis.png")
    plt.show()