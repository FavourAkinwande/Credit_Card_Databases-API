const { MongoClient } = require('mongodb');

// Use your actual MongoDB Atlas connection string
const uri = 'mongodb+srv://fakinwande:M50xQRyrwpnBGG9j@cluster0.f8wa06y.mongodb.net/';

const client = new MongoClient(uri);

async function connectDB() {
  try {
    await client.connect();
    console.log('Connected to MongoDB Atlas!');
    // You can now use `client.db()` to access your database
  } catch (err) {
    console.error('Connection error:', err);
  } finally {
    await client.close(); // Close the connection when done
  }
}

connectDB();
