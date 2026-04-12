import { useState } from "react";

function App() {
  const [product, setProduct] = useState("");
  const [brand, setBrand] = useState("");
  const [audience, setAudience] = useState("");
  const [description, setDescription] = useState("");
  const [imagePrompt, setImagePrompt] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateCampaign = async () => {
    if (!product || !audience) {
      alert("Enter product and audience");
      return;
    }

    setLoading(true);

    // 🔥 IMPORTANT FIX: force reset before new request
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
        // 🔥 force new object reference
        setResult({ ...data.data });
      }

    } catch (err) {
      console.error(err);
      alert("Error occurred");
    }

    setLoading(false);
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

  const handleReset = () => {
    setResult(null);
  };

  return (
    <div style={styles.container}>

      <h1 style={styles.title}>AI Marketing Agent</h1>

      {/* INPUTS ALWAYS VISIBLE */}
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
          {loading ? "Generating..." : "Generate Ad"}
        </button>
      </div>

      {/* LOADING */}
      {loading && <p style={{ marginTop: "20px" }}>Generating campaign...</p>}

      {/* OUTPUT */}
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
                  <span key={i} style={styles.tag}>{tag}</span>
                ))}
            </div>

            <p style={styles.cta}>
              {result.content.cta}
            </p>

          </div>

          {/* IMAGE */}
          {result.image_path && (
            <div style={styles.imageWrapper}>

              <img
                src={`http://127.0.0.1:8000${result.image_path}`}
                alt="Generated"
                style={styles.image}
              />

              <button onClick={handleDownload} style={styles.downloadBtn}>
                Download Image
              </button>

            </div>
          )}

          {/* BACK BUTTON */}
          <button onClick={handleReset} style={styles.backBtn}>
            Clear Output
          </button>

        </div>
      )}

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
  }
};