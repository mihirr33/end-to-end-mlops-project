import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#2563eb", "#ef4444"];

function AnalyticsChart() {

  const data = [
    { name: "No Churn", value: 73 },
    { name: "Churn", value: 27 },
  ];

  return (

    <div className="chart-card">

      <h2>Prediction Distribution</h2>

      <ResponsiveContainer width="100%" height={320}>

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            outerRadius={110}
            label
          >

            {
              data.map((entry,index)=>(

                <Cell
                  key={index}
                  fill={COLORS[index]}
                />

              ))
            }

          </Pie>

          <Tooltip/>

        </PieChart>

      </ResponsiveContainer>

    </div>

  );

}

export default AnalyticsChart;