// import React, { useEffect, useRef } from 'react';
// import { createChart } from 'lightweight-charts';

// function Chart({ data }) {
//   const chartContainerRef = useRef();

//   useEffect(() => {
//     const chart = createChart(chartContainerRef.current, { width: 600, height: 300 });
//     const lineSeries = chart.addLineSeries();
//     lineSeries.setData(data);

//     return () => chart.remove();
//   }, [data]);

//   return <div ref={chartContainerRef} />;
// }

// export default Chart;