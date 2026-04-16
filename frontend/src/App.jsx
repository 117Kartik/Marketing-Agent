import { useState } from "react";

function App() {
  const [product, setProduct] = useState("");
  const [brand, setBrand] = useState("");
  const [audience, setAudience] = useState("");
  const [description, setDescription] = useState("");
  const [imagePrompt, setImagePrompt] = useState("");

  const [loading, setLoading] = useState(false);  

  const [activeTab, setActiveTab] = useState("generate");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [file, setFile] = useState(null);

  const generateCampaign = async () => {
    if (!product || !audience) {
      alert("Enter product and audience");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/generate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          product,
          brand,
          audience,
          description,
          image_prompt: imagePrompt
        })
      });

      const data = await res.json();

      if (data.success) {
        setResult({ ...data.data });
      }

    } catch (err) {
      console.error(err);
      alert("Error occurred");
    }

    setLoading(false);
  };

  // ✅ FIXED: outside function
  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/history/");
      const data = await res.json();

      if (data.success) {
        setHistory(data.data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ FIXED: outside function
  const loadFromHistory = (item) => {
    setProduct(item.product);
    setBrand(item.brand);
    setAudience(item.audience);
    setDescription(item.description);
    setImagePrompt(item.image_prompt);

    setResult(item);
  };

  const handleDownload = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000${result.image_path}`);
      const blob = await res.blob();

      const fileURL = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = fileURL;
      link.setAttribute("download", "marketing_image.jpg");

      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      window.URL.revokeObjectURL(fileURL);

    } catch (err) {
      console.error(err);
      alert("Download failed");
    }
  };


  const sendEmails = async () => {
    if (!file) {
      alert("Upload CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/publish/", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      alert(data.message || data.error);

    } catch (err) {
      console.error(err);
      alert("Failed to send emails");
    }
  };
  const handleReset = () => {
    setResult(null);
  };

  return (
  <div style={styles.appLayout}>

    {/* SIDEBAR */}
    <div style={styles.sidebar}>
      <h2 style={{ marginBottom: "20px" }}>Dashboard</h2>

      <div onClick={() => setActiveTab("generate")} style={styles.navItem}>
        Generate
      </div>

      <div
        onClick={() => {
          setActiveTab("history");
          fetchHistory();
        }}
        style={styles.navItem}>
        History
      </div>

      <div onClick={() => setActiveTab("publish")} style={styles.navItem}>
        Publish
      </div>
    </div>

    {/* MAIN */}
    <div style={styles.mainContent}>

      <div style={styles.container}>

        {/* TOP BAR */}
        <div style={styles.topBar}>
          <h1 style={styles.titleCentered}>AI Marketing Agent</h1>
          <div style={styles.rightControls}></div>

          <div style={styles.rightControls}>
            {activeTab === "publish" && (
              <>
                <button onClick={sendEmails} style={styles.sendBtn}>
                  Send Emails
                </button>

                <input
                  type="file"
                  onChange={(e) => setFile(e.target.files[0])}
                  style={styles.fileInput}
                />
              </>
            )}
          </div>
        </div>

        {/* ================= GENERATE ================= */}
        {activeTab === "generate" && (
          <>

            <div style={styles.inputCard}>
              <input
                placeholder="Product"
                value={product}
                onChange={(e) => setProduct(e.target.value)}
              />

              <input
                placeholder="Brand"
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
              />

              <input
                placeholder="Audience"
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
              />

              <textarea
                placeholder="Product description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />

              <input
                placeholder="Image style (optional)"
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
              />

              <button onClick={generateCampaign} style={styles.button}>
                {loading ? "Generating..." : "Generate"}
              </button>
            </div>

            {loading && (
              <p style={{ marginTop: "20px" }}>
                Generating campaign...
              </p>
            )}

            {result && result.content && (
              <div key={Date.now()} style={styles.outputWrapper}>

                <div style={styles.outputBox}>
                  <h2 style={styles.headline}>
                    {result.content.headline}
                  </h2>

                  <p style={styles.caption}>
                    {result.content.description}
                  </p>

                  <div style={styles.hashtags}>
                    {Array.isArray(result.content.hashtags) &&
                      result.content.hashtags.map((tag, i) => (
                        <span key={i} style={styles.tag}>
                          {tag}
                        </span>
                      ))}
                  </div>

                  <p style={styles.cta}>
                    {result.content.cta}
                  </p>
                </div>

                {result.image_path && (
                  <div style={styles.imageWrapper}>
                    <img
                      src={`http://127.0.0.1:8000${result.image_path}`}
                      alt="Generated"
                      style={styles.image}
                    />

                    <button
                      onClick={handleDownload}
                      style={styles.downloadBtn}
                    >
                      Download Image
                    </button>
                  </div>
                )}

                <button onClick={handleReset} style={styles.backBtn}>
                  Clear Output
                </button>

              </div>
            )}
          </>
        )}

        {/* ================= HISTORY ================= */}
        {activeTab === "history" && (
          <>
            {history.length > 0 && (
              <div style={styles.historyContainer}>
                <h3 style={{ marginBottom: "10px" }}>History</h3>

                <div style={styles.historyGrid}>
                  {history.map((item, i) => (
                    <div
                      key={i}
                      style={styles.historyCard}
                      onClick={() => {
                        loadFromHistory(item);
                        setActiveTab("generate");
                      }}
                      onMouseEnter={(e) =>
                        (e.currentTarget.style.transform = "scale(1.05)")
                      }
                      onMouseLeave={(e) =>
                        (e.currentTarget.style.transform = "scale(1)")
                      }
                    >
                      {item.image_path && (
                        <img
                          src={`http://127.0.0.1:8000${item.image_path}`}
                          alt="history"
                          style={styles.historyImage}
                        />
                      )}

                      <div style={styles.historyText}>
                        <h4 style={{ margin: "5px 0" }}>
                          {item.content?.headline || "No headline"}
                        </h4>

                        <p style={{ fontSize: "12px", color: "#94a3b8" }}>
                          {item.product} • {item.audience}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        {/* ================= PUBLISH ================= */}
        {activeTab === "publish" && (
          <div style={{ marginTop: "40px" }}>
            <p>Upload CSV and send campaign emails.</p>
          </div>
        )}

      </div>
    </div>
  </div>
);
}

export default App;

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "40px",
    background: "#0f172a",
    color: "white",
    minHeight: "100vh"
  },

  title: {
    fontSize: "36px",
    marginBottom: "20px"
  },

  inputCard: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    width: "350px",
    background: "#1e293b",
    padding: "20px",
    borderRadius: "10px"
  },

  button: {
    padding: "10px",
    background: "#2563eb",
    border: "none",
    color: "white",
    borderRadius: "6px",
    cursor: "pointer"
  },

  outputWrapper: {
    marginTop: "40px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    width: "100%"
  },

  outputBox: {
    width: "600px",
    background: "rgba(30, 41, 59, 0.6)",
    backdropFilter: "blur(10px)",
    padding: "25px",
    borderRadius: "12px"
  },

  headline: {
    fontSize: "28px",
    fontWeight: "bold"
  },

  caption: {
    marginTop: "10px",
    color: "#cbd5f5"
  },

  hashtags: {
    marginTop: "10px"
  },

  tag: {
    marginRight: "10px",
    color: "#60a5fa"
  },

  cta: {
    marginTop: "15px",
    fontWeight: "bold"
  },

  imageWrapper: {
    marginTop: "20px",
    width: "600px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  

  image: {
    width: "100%",
    borderRadius: "12px"
  },

  downloadBtn: {
    marginTop: "10px",
    padding: "10px",
    background: "#1e40af",
    color: "white",
    border: "none",
    borderRadius: "6px"
  },

  backBtn: {
    marginTop: "20px",
    padding: "10px",
    background: "#374151",
    color: "white",
    border: "none",
    borderRadius: "6px"
  },

  historyContainer: {
  marginTop: "40px",
  width: "80%",
  maxWidth: "900px"
},

historyGrid: {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
  gap: "15px"
},

historyCard: {
  background: "#1e293b",
  borderRadius: "10px",
  overflow: "hidden",
  cursor: "pointer",
  transition: "0.3s",
},

historyImage: {
  width: "100%",
  height: "120px",
  objectFit: "cover"
},

historyText: {
  padding: "10px"
},
historyCard: {
  background: "#1e293b",
  borderRadius: "10px",
  overflow: "hidden",
  cursor: "pointer",
  transition: "0.3s ease",
},

sendBtn: {
  padding: "10px 15px",
  background: "#16a34a",
  border: "none",
  color: "white",
  borderRadius: "6px",
  cursor: "pointer"
},
sendBtn: {
  padding: "10px 15px",
  background: "#16a34a",
  border: "none",
  color: "white",
  borderRadius: "6px",
  cursor: "pointer",
  transition: "0.3s"
},
container: {
  minHeight: "100vh",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "40px",
  background: "linear-gradient(135deg, #0f172a, #1e293b)"
},

topBar: {
  width: "100%",
  maxWidth: "1000px",
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center", 
  position: "relative",
  marginBottom: "30px"
},

leftSpace: {
  width: "120px"
},

title: {
  fontSize: "34px",
  fontWeight: "bold",
  textAlign: "center"
},

rightControls: {
  position: "absolute",
  right: "0",
  top: "0",
  display: "flex",
  flexDirection: "column",
  gap: "10px"
},

sendBtn: {
  padding: "10px 16px",
  background: "#22c55e",
  border: "none",
  color: "white",
  borderRadius: "8px",
  cursor: "pointer",
  fontWeight: "bold"
},

fileInput: {
  fontSize: "12px",
  color: "white"
},

inputCard: {
  background: "rgba(30, 41, 59, 0.6)",
  backdropFilter: "blur(12px)",
  padding: "20px",
  borderRadius: "16px",
  width: "350px",
  display: "flex",
  flexDirection: "column",
  gap: "12px",
  boxShadow: "0 8px 30px rgba(0,0,0,0.4)"
},

outputBox: {
  background: "rgba(30, 41, 59, 0.6)",
  backdropFilter: "blur(15px)",
  padding: "25px",
  borderRadius: "16px",
  boxShadow: "0 8px 30px rgba(0,0,0,0.4)"
},
button: {
  padding: "10px",
  background: "#2563eb",
  border: "none",
  color: "white",
  borderRadius: "8px",
  cursor: "pointer",
  transition: "0.3s"
},

appLayout: {
  display: "flex",
  height: "100vh",
  background: "#0f172a",
  color: "white"
},

sidebar: {
  width: "220px",
  background: "#020617",
  padding: "20px",
  borderRight: "1px solid #1e293b"
},

navItem: {
  padding: "10px",
  marginBottom: "10px",
  cursor: "pointer",
  borderRadius: "6px",
  background: "#1e293b"
},

mainContent: {
  flex: 1,
  overflowY: "auto"
},

titleCentered: {
  width: "100%",
  textAlign: "center",
  fontSize: "32px",
  fontWeight: "bold"
},

};