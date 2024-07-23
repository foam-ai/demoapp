export const getProductData = async () => {
  try {
    const response = await fetch('/api/getProductData');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching product data:', error);
    return { productData: [], applicationMap: {} };
  }
};
