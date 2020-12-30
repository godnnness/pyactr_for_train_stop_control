# /usr/bin/env python
# -*- coding: UTF-8 -*-
import pyactr as actr
from simpy.core import EmptySchedule
import xlrd
actr.chunktype("stoptrain_goal", "state")
actr.chunktype("stopfortrain", "action curv nexv curd")

parser = actr.ACTRModel(subsymbolic=True,
                       activation_trace=True,
                       retrieval_threshold=-80,
                       partial_matching=True,
                       optimized_learning = True,
                        production_compilation=True,
                    )
dm = parser.decmem
g = parser.goal
imaginal = parser.set_goal(name="imaginal", delay=0.2)
# 用于判断推荐速度是否低于实际速度+1.3889
nvGeCvplus13889=parser.set_goal("nvGeCvplus13889")
parser.goals["nvGeCvplus13889"].add(actr.chunkstring(string="isa DistLeNeg03 value None"))
# 用于判断与停车标得距离是否大于-0.3
distLeNeg03=parser.set_goal("distGeNeg03")
parser.goals["distGeNeg03"].add(actr.chunkstring(string="isa DistGeNeg03 value None"))
with open("chunk.csv", "w") as f:
    workbook = xlrd.open_workbook('C:\\Users\\syl\\Desktop\\trainforactr\\myDriveForChunk.xlsx')
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
    carspeed, dangwei, tuijianspeed, dis_juli = [], [], [], []
    for i in booksheet.col_values(0):
        dangwei.append(int(i))
    for i in booksheet.col_values(1):
        carspeed.append(int(i))
    for i in booksheet.col_values(2):
        tuijianspeed.append(int(i - 3))
    for i in booksheet.col_values(3):
        if i <= 0:
            i = 1e-8
        dis_juli.append(int(i))
    # print("dangwei:\n", dangwei)
    # print("carspeed:\n", carspeed)
    # print("tuijianspeed:\n", tuijianspeed)
    # print("dis_juli:\n", dis_juli)
    for i in range(len(dangwei)):
        # 初始化陈述性记忆

        dm.add(actr.chunkstring(string="""
            isa stopfortrain
            action """ + str(dangwei[i]) + """
            curv """ + str(carspeed[i]) + """
            nexv """ + str(tuijianspeed[i]) + """
            curd """ + str(dis_juli[i]) + """
        """))

g.add(actr.chunkstring(string="""
    isa stoptrain_goal
    state start
"""))

imaginal.add(actr.chunkstring(string="""
    isa stopfortrain
    curv 30
    nexv 31
    curd 2000
"""))

parser.productionstring(name="开始驾驶", string="""
    =g>
    isa stoptrain_goal
    state start
    =imaginal>
    isa stopfortrain
    curv =cv
    nexv =nv
    curd =cd
    ==>
    =g>
    isa stoptrain_goal
    state startretriveANDinitjudge
    +retrieval>
    isa stopfortrain
    curv =cv
    nexv =nv
    curd =cd

""")
parser.productionstring(name="当前速度<推荐速度+1.3889 and 当前距离>0", string="""
    =g>
    isa stoptrain_goal
    state startretriveANDinitjudge
    =nvGeCvplus13889>
    isa NvGeCvplus13889
    value True
    =distGeNeg03>
    isa DistGeNeg03
    value True
    ==>
    =g>
    isa stoptrain_goal
    state startretrive
""")


parser.productionstring(name="当前速度>推荐速度+1.3889 and 当前距离>0", string="""
    =g>
    isa stoptrain_goal
    state startretriveANDinitjudge
    =nvGeCvplus13889>
    isa NvGeCvplus13889
    value None
    =distGeNeg03>
    isa DistGeNeg03
    value True
    ==>
    =g>
    isa stoptrain_goal
    state lowaction
    
""")
parser.productionstring(name="当前速度<推荐速度+1.3889 and 当前距离<0", string="""
    =g>
    isa stoptrain_goal
    state startretriveANDinitjudge
    =nvGeCvplus13889>
    isa NvGeCvplus13889
    value True
    =distGeNeg03>
    isa DistGeNeg03
    value None
    ==>
    =g>
    isa stopfortrain
    action 7
    !g>
    show action
    =g>
    isa stoptrain_goal
    state stop
""")
parser.productionstring(name="结束", string="""
    =g>
    isa stoptrain_goal
    state stop
    ==>
    ~g>
""")

parser.productionstring(name="回忆成功", string="""
    =g>
    isa stoptrain_goal
    state startretrive
    =retrieval>
    isa stopfortrain
    action =a
    ==>
    =g>
    isa stoptrain_goal
    state stop 
    ~retrieval>
""",reward=10)

parser.productionstring(name="回忆失败", string="""
    =g>
    isa stoptrain_goal
    state startretrive
    ?retrieval>
    state error
    ==>
    ~g>
    ~retrieval>
""")

if __name__ == "__main__":
    parser_sim = parser.simulation()
    # run the simulation
    while True:
        # print ("------------------------------------------------")
        try:
            # do one step in simulation
            parser_sim.step()
        except EmptySchedule:
            # unless there are no steps, in which case - break
            break

        if parser.goals['imaginal'] and int(parser.goals['imaginal'].copy().pop()[3][1].__repr__())+1.3889>int(parser.goals['imaginal'].copy().pop()[2][1].__repr__()):
            # 如果当前速度小于推荐速度，则不匹配
            # print("触发条件语句")
            # print("推荐速度与实际速度的差值：",int(parser.goals['imaginal'].copy().pop()[3][1].__repr__())-int(parser.goals['imaginal'].copy().pop()[2][1].__repr__()))
            parser.goals["nvGeCvplus13889"].add(actr.chunkstring(string="isa NvGeCvplus13889 value True"))
        else:
            parser.goals["nvGeCvplus13889"].add(actr.chunkstring(string="isa NvGeCvplus13889 value None"))

        if parser.goals['imaginal'] and int(parser.goals['imaginal'].copy().pop()[1][1].__repr__())>0:
            # print("剩余距离大于-0.3")
            parser.goals["distGeNeg03"].add(actr.chunkstring(string="isa DistGeNeg03 value True"))
        else:
            # print("剩余距离小于-0.3")
            parser.goals["distGeNeg03"].add(actr.chunkstring(string="isa DistGeNeg03 value None"))
        # print("parser.goals['imaginal'].copy().pop()[2][1]：", parser.goals['imaginal'].copy().pop()[2][1])
        # print("推荐速度是否大于实际速度：",parser.goals['imaginal'].copy().pop()[3][1] > parser.goals['imaginal'].copy().pop()[2][1])
        # # print("\nDeclarative memory at the end of the simulation:")
        # print(dm)
        # print("\ngoal buffer:\n--> ", parser.goals["g"])
        # print("\nimaginal buffer:\n--> ", parser.goals["imaginal"])

        if parser.retrieval:
            action= int(parser.retrieval.copy().pop()[0][1].__repr__())
            print("\naction of retrieval buffer: ", action)

