## 推荐模板
- [官方模板](https://matplotlib.org/gallery/index.html)
- [Top 50 matplotlib Visualizations](https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/)


### 多个(子)图
- 不同的图(多个窗口中打开)
```python
plt.fig(1)	# 当前在图1
plt.plot()

plt.fig(2)	# 当前在图2
plt.plot()
```

- 一个窗口中多个子图
```python
plt.fig(1)	# 当前在图1
plt.subplots(1,2,1)	# 图1包含1行2列，当前在第1列
plt.plot()

plt.fig(1)	# 当前还在图1，可以不指明
plt.subplots(1,2,2)	# 图1包含1行2列，当前在第2列
plt.plot()
```

### 刻度值、x、y、label的指定
```python
x = list(range(10))
y1 = np.random.randint(1, 10, 10)
y2 = np.random.randint(10, 20, 10)

plt.figure(1)
plt.xlabel('area')  # x轴名称
plt.ylabel('price')
plt.xticks(x, ['tick%d' % x for x in range(10)])  # 刻度值
plt.plot(x, y1, 'g*--', label='price1')
plt.plot(x, y2, 'ro-.', label='price2')
plt.legend()
plt.show()
```