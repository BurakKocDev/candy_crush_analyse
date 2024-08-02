import pandas as pd 


data = pd.read_csv('candy_crush.csv')

print(data.head(5))
print(data.info)
print(data.describe)
print(data.isna().sum())
print(data.shape)



# İlk 15 seviyeyi filtreleyelim
first_15_levels = data[data['level'] <= 15]

# Her seviye için ortalama deneme sayısı ve başarı oranını hesaplayalım
difficulty_analysis = first_15_levels.groupby('level').agg({
    'num_attempts': 'mean',
    'num_success': 'mean'
}).reset_index()

# Başarı oranını yüzde olarak ifade edelim
difficulty_analysis['success_rate'] = difficulty_analysis['num_success'] * 100

# Sonuçları gösterelim
difficulty_analysis.drop(columns='num_success', inplace=True)
difficulty_analysis.rename(columns={'num_attempts': 'avg_attempts'}, inplace=True)
difficulty_analysis



import matplotlib.pyplot as plt
import seaborn as sns

# Deneme sayısı dağılımı histogramı
plt.figure(figsize=(12, 6))
sns.histplot(first_15_levels['num_attempts'], bins=20, kde=True)
plt.title('Deneme Sayısı Dağılımı')
plt.xlabel('Deneme Sayısı')
plt.ylabel('Frekans')
plt.show()

# Her seviyenin deneme sayısı ve başarı oranı çizgi grafiği
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Seviye')
ax1.set_ylabel('Ortalama Deneme Sayısı', color=color)
ax1.plot(difficulty_analysis['level'], difficulty_analysis['avg_attempts'], color=color, marker='o', label='Ortalama Deneme Sayısı')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Başarı Oranı (%)', color=color)
ax2.plot(difficulty_analysis['level'], difficulty_analysis['success_rate'], color=color, marker='x', linestyle='--', label='Başarı Oranı (%)')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Seviye Bazında Deneme Sayısı ve Başarı Oranı')
plt.show()


# Deneme sayısı ve başarı oranı arasındaki korelasyon
correlation = difficulty_analysis[['avg_attempts', 'success_rate']].corr()
print("Deneme Sayısı ve Başarı Oranı Arasındaki Korelasyon:")
print(correlation)


# Seviyelere göre başarı oranı boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='level', y='success_rate', data=difficulty_analysis)
plt.title('Seviye Bazında Başarı Oranı')
plt.xlabel('Seviye')
plt.ylabel('Başarı Oranı (%)')
plt.show()


# Scatter plot
plt.figure(figsize=(12, 6))
sns.scatterplot(x='avg_attempts', y='success_rate', data=difficulty_analysis)
plt.title('Deneme Sayısı ve Başarı Oranı Arasındaki İlişki')
plt.xlabel('Ortalama Deneme Sayısı')
plt.ylabel('Başarı Oranı (%)')
plt.show()


# Başarı oranının dağılımı histogramı
plt.figure(figsize=(12, 6))
sns.histplot(difficulty_analysis['success_rate'], bins=10, kde=True)
plt.title('Başarı Oranı Dağılımı')
plt.xlabel('Başarı Oranı (%)')
plt.ylabel('Frekans')
plt.show()

# Seviyeleri zorluklarına göre sınıflandıralım
def categorize_difficulty(row):
    if row['success_rate'] < 50:
        return 'Zor'
    elif 50 <= row['success_rate'] <= 75:
        return 'Orta'
    else:
        return 'Kolay'

difficulty_analysis['difficulty'] = difficulty_analysis.apply(categorize_difficulty, axis=1)

# Zorluk seviyelerini gösterelim
print(difficulty_analysis[['level', 'avg_attempts', 'success_rate', 'difficulty']])


# Örneğin 'dt' sütunu varsa
data['dt'] = pd.to_datetime(data['dt'])

# Zaman içinde ortalama deneme sayısı
time_series_attempts = data.groupby('dt').agg({'num_attempts': 'mean'}).reset_index()

plt.figure(figsize=(12, 6))
plt.plot(time_series_attempts['dt'], time_series_attempts['num_attempts'], marker='o')
plt.title('Zaman İçinde Ortalama Deneme Sayısı')
plt.xlabel('Tarih')
plt.ylabel('Ortalama Deneme Sayısı')
plt.show()

# Zaman içinde ortalama başarı oranı
time_series_success_rate = data.groupby('dt').agg({'num_success': 'mean'}).reset_index()
time_series_success_rate['success_rate'] = time_series_success_rate['num_success'] * 100

plt.figure(figsize=(12, 6))
plt.plot(time_series_success_rate['dt'], time_series_success_rate['success_rate'], marker='x', color='red')
plt.title('Zaman İçinde Ortalama Başarı Oranı')
plt.xlabel('Tarih')
plt.ylabel('Başarı Oranı (%)')
plt.show()




