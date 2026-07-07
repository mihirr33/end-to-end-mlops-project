function PredictionHistory({ history }) {
  return (
    <div className="history-card">

      <h2>Prediction History</h2>

      <table>

        <thead>
          <tr>
            <th>#</th>
            <th>Prediction</th>
            <th>Confidence</th>
            <th>Risk</th>
          </tr>
        </thead>

        <tbody>

          {history.length === 0 ? (

            <tr>
              <td colSpan="4">
                No Predictions Yet
              </td>
            </tr>

          ) : (

            history.map((item, index) => (

              <tr key={index}>

                <td>{index + 1}</td>

                <td>{item.prediction}</td>

                <td>{item.confidence}%</td>

                <td>{item.risk}</td>

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  );
}

export default PredictionHistory;