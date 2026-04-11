import { useState } from "react";

function App() {
  const [product, setProduct] = useState("");
  const [audience, setAudience] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateCampaign = async () => {
    if (!product || !audience) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/generate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product, audience }),
      });

      const data = await response.json();
      setResult(data.data);
    } catch (error) {
      console.error(error);
      alert("Error generating campaign");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI Marketing Agent</h1>

      <input
        placeholder="Enter product"
        value={product}
        onChange={(e) => setProduct(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Enter audience"
        value={audience}
        onChange={(e) => setAudience(e.target.value)}
      />
      <br /><br />

      <button onClick={generateCampaign}>
        {loading ? "Generating..." : "Generate Campaign"}
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>{result.content.headline}</h2>

          <p>{result.content.caption}</p>

          <h3>Hashtags:</h3>
          {result.content.hashtags.map((tag, i) => (
            <p key={i}>{tag}</p>
          ))}

          <h3>CTA:</h3>
          <p>{result.content.cta}</p>

          <h3>Image:</h3>
          <p>{result.image_path}</p>
        </div>
      )}
    </div>
  );
}

export default App;
