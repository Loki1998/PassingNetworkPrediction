这个项目是2019年北京邮电大学社会网络分析与算法研究的项目

项目名称：基于链接预测的传球网络分析

项目介绍：
本项目使用2015-2016年度UEFA（欧洲足球协会联盟 Union of European Football Associations）
官方提供的数据，进行二次处理之后，形成一个传球网络，分析了这个传球网络的特征。
在可视化我们的网络过程中，我们使用了Gephi进行可视化以及简单的网络特征的分析。
进一步的，我们使用了线性预测模型对比赛中的传球进行预测，得到一个新的传球网络。
最后，我们将预测得到的传球网络和实际场次的网络进行对比，并评价我们的预测模型。

项目结构：
* `data`:这个文件夹里包含了原始数据以及我们处理之后的数据。
* `gephi`:这个文件夹里包含了使用Gephi进行可视化的测试文件。
* `predicted`:这个文件夹包含了预测模型的输出结果，对输出文件处理后倒入到Gephi中，可以得到我们预测的网络。
* `prediction`:这个文件夹包含了我们的模型代码，有baseline和pdPrediction两种预测方式，其中baseline对应基础模型，
参数是由所有结果取平均得到，pdPrediction使用线性回归模型的到的权重，在这个目录下用python2环境，添加相应的依赖包即可运行。
* `scripts`:这个文件夹主要存放了对数据的处理文件，从原始数据中提取出我们使用的数据特征。

模型结果：我们线性回归模型结果高出基础模型10.49%
 
