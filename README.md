# TrelloAnalyzer
TrelloAnalyzer lets you measure time-cost of your project as well as track your team's velocity and efficiency those recorded in trello.

---

### 计算说明：
- **total**：总预计工时。当前 list 中卡片的预计工时总和。
- **none**：无工时卡片数。当前 list 中无工时的卡片数。
- **new**：总新增工时。当前 list 中 label 为“新增”的卡片实际工时总和。
- **urgent**：总紧急工时。当前 list 中 label 为“紧急”的卡片实际工时总和。
- **plan_hours**：预计工时。当前 list 中同一作者的卡片预估工时（ title 中第一个括号中时间）总和。
- **actual_hours**：实际工时。当前 list 中同一作者的卡片实际工时（ title 中第二个括号中时间，若没有，取第一个括号中的预计工时加和）总和
- **new_work_hours**：新增任务实际工时。取 label 为“新增”及“紧急”的同一作者的卡片实际工时（ title 中第二个括号中时间，若没有，取第一个括号中的预计工时加和）总和


### 运行说明：
- **./analyse.py board**: Statistics the card information in the current list
- **./analyse.py new_iteration**: Save a snapshot before you start an iteration
- **./analyse.py daily_cards**: Save a snapshot for each day after the iteration begins
- **./analyse.py cards_stat**: Use the snapshot to count new cards
- **./analyse.py burn_down**: Draw a iteration's burn down chart