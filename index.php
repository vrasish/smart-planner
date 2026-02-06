<?php
// Database connection
$conn = new mysqli("localhost", "root", "", "smartplanner", 3306);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get today's plan with task details
$today = date('Y-m-d');
$sql = "
    SELECT 
        dp.id,
        dp.task_order,
        t.title,
        t.duration_minutes,
        t.priority,
        t.deadline
    FROM daily_plan dp
    JOIN tasks t ON dp.task_id = t.id
    WHERE dp.plan_date = '$today'
    ORDER BY dp.task_order
";

$result = $conn->query($sql);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Planner - Today's Plan</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 Smart Planner</h1>
            <p class="date"><?php echo date('l, F j, Y'); ?></p>
        </header>

        <div class="plan-section">
            <?php if ($result->num_rows > 0): ?>
                <h2>Today's Plan</h2>
                <div class="tasks-list">
                    <?php 
                    $total_minutes = 0;
                    while($row = $result->fetch_assoc()): 
                        $total_minutes += $row['duration_minutes'];
                        $hours = floor($row['duration_minutes'] / 60);
                        $minutes = $row['duration_minutes'] % 60;
                        $time_display = $hours > 0 ? "{$hours}h {$minutes}m" : "{$minutes}m";
                    ?>
                        <div class="task-card">
                            <div class="task-order"><?php echo $row['task_order']; ?></div>
                            <div class="task-content">
                                <h3><?php echo htmlspecialchars($row['title']); ?></h3>
                                <div class="task-details">
                                    <span class="duration">⏱️ <?php echo $time_display; ?></span>
                                    <span class="priority priority-<?php echo $row['priority']; ?>">
                                        Priority: <?php echo $row['priority']; ?>
                                    </span>
                                    <span class="deadline">📅 Due: <?php echo date('M j', strtotime($row['deadline'])); ?></span>
                                </div>
                            </div>
                        </div>
                    <?php endwhile; ?>
                </div>
                <div class="summary">
                    <p>Total time: <?php echo floor($total_minutes / 60); ?>h <?php echo $total_minutes % 60; ?>m</p>
                </div>
            <?php else: ?>
                <div class="no-plan">
                    <p>No plan generated for today.</p>
                    <p>Run <code>python planner.py</code> to generate your plan!</p>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
<?php
$conn->close();
?>
