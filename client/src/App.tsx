import { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [originalData, setOriginalData] = useState({});
  const [predictionData, setPredictionData] = useState([]);

  const colors = [
    'rgba(255, 99, 132, 0.5)', // Cakalang
    'rgba(54, 162, 235, 0.5)', // Tongkol
    'rgba(255, 206, 86, 0.5)', // Tuna
    'rgba(75, 192, 192, 0.5)', // Udang
  ];

  const options: Intl.DateTimeFormatOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };

  
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1); // Add 1 day to today's date

  const formattedDate = tomorrow.toLocaleDateString('en-US', options); // Format the date

  useEffect(() => {
    fetch('110.239.71.252:1414/api/data')
      .then(res => res.json())
      .then(data => setOriginalData(data));

    fetch('110.239.71.252:1414/api/predictions')
      .then(res => res.json())
      .then(data => setPredictionData(data));
  }, []);

  const sortedPredictionData = predictionData.slice().sort((a, b) => {
    const fishTypeA = Object.keys(a)[2].split('_')[0]; // Ambil nama ikan dari key pertama (misal: Cakalang_RF)
    const fishTypeB = Object.keys(b)[2].split('_')[0];
    return fishTypeA.localeCompare(fishTypeB); // Urutkan secara alfabetis
  });

  const originalChartData = { 
    labels: Object.keys(originalData), // Tahun sebagai label
    datasets: [
      {
        label: 'Cakalang',
        data: Object.values(originalData).map((value: unknown) => {
          if (Array.isArray(value)) { 
            return value.reduce((sum: any, item: { Cakalang: any; }) => sum + item.Cakalang, 0);
          } else {
            return 0; // Or some default value if it's not an array
          }
        }),
        backgroundColor: colors[0], 
      },
      {
        label: 'Tongkol',
        data: Object.values(originalData).map((value: unknown) => {
          if (Array.isArray(value)) { 
            return value.reduce((sum: any, item: { Tongkol: any; }) => sum + item.Tongkol, 0);
          } else {
            return 0; // Or some default value if it's not an array
          }
        }),
        backgroundColor: colors[0], 
      },
      {
        label: 'Tuna',
        data: Object.values(originalData).map((value: unknown) => {
          if (Array.isArray(value)) { 
            return value.reduce((sum: any, item: { Tuna: any; }) => sum + item.Tuna, 0);
          } else {
            return 0; // Or some default value if it's not an array
          }
        }),
        backgroundColor: colors[0], 
      },
      {
        label: 'Udang',
        data: Object.values(originalData).map((value: unknown) => {
          if (Array.isArray(value)) { 
            return value.reduce((sum: any, item: { Udang: any; }) => sum + item.Udang, 0);
          } else {
            return 0; // Or some default value if it's not an array
          }
        }),
        backgroundColor: colors[0], 
      },

      // ... dataset lain untuk jenis ikan lainnya
    ],
    options: {
      responsive: true, // Agar chart responsif terhadap perubahan ukuran layar
      maintainAspectRatio: false, // Agar chart bisa berubah ukuran sesuai wadah
      plugins: {
        legend: {
          position: 'top', // Posisi legenda di atas chart
        },
      },
      scales: {
        x: {
          ticks: {
            font: {
              size: 10, // Ukuran font label sumbu x
            },
          },
        },
        y: {
          ticks: {
            font: {
              size: 10, // Ukuran font label sumbu y
            },
          },
        },
      },
    },
  };

  // ... (opsional) buat chartData untuk predictionData dengan cara serupa

  return (
    <>
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">Data dan Prediksi Produksi Ikan</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Chart */}
        <div>
          <h2 className="text-xl font-semibold mb-2">Data Produksi Ikan dari Tahun 2017-2021</h2>
          <Bar data={originalChartData} />
        </div>

        {/* Tabel Prediksi */}
      <div>
      <h2 className="text-xl font-semibold mb-2">Prediksi Produksi Ikan Hari Berikutnya</h2>
      <table className="table-auto border-collapse w-full">
        <thead>
          <tr>
            <th className="border px-4 py-2">Tanggal</th> {/* Tanggal di atas */}

          </tr>
        </thead>
        <tbody>
          {sortedPredictionData.length > 0 && (
            <tr>
              <td className="border px-4 py-2">{formattedDate}</td>
              
            </tr>
          )}
        </tbody>

        <thead> {/* Tambahkan header baru untuk jenis ikan dan prediksi */}
          <tr>
            <th className="border px-4 py-2">Jenis Ikan</th>
            <th className="border px-4 py-2">Prediksi (RF)</th>
          </tr>
        </thead>
        <tbody>
          {sortedPredictionData.length > 0 && (
            Object.keys(sortedPredictionData[0]).slice(2).map((fishType) => (
              <tr key={fishType}>
                <td className="border px-4 py-2">{fishType.split('_')[0]}</td>
                <td className="border px-4 py-2">{sortedPredictionData[0][fishType]}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
    </div>
  </div>
  </>
  );
}

export default App;
