import React from 'react';

/**
 * GreetingCard Component
 * A simple component that displays a greeting message.
 *
 * @param {object} props - The properties passed to the component.
 * @param {string} props.name - The name of the person to greet.
 * @param {string} [props.message="Hello"] - An optional custom message.
 */
function GreetingCard({ name, message = "Hello" }) {
  if (!name) {
    return (
      <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', backgroundColor: '#f9f9f9', maxWidth: '300px', margin: '20px auto' }}>
        <p style={{ color: 'red', fontWeight: 'bold' }}>Error: Name prop is required.</p>
      </div>
    );
  }

  return (
    <div style={{
      padding: '20px',
      border: '1px solid #ddd',
      borderRadius: '8px',
      backgroundColor: '#fff',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      maxWidth: '300px',
      margin: '20px auto',
      textAlign: 'center'
    }}>
      <h2 style={{ color: '#333', marginBottom: '10px' }}>{message}, {name}!</h2>
      <p style={{ color: '#666', fontSize: '0.9em' }}>
        Welcome to this React component example.
      </p>
    </div>
  );
}

/*
// --- How to use this component in a React App ---

// 1. Import it into another component or your App.js:
// import GreetingCard from './GreetingCard';

// 2. Render it with props:
// function App() {
//   return (
//     <div>
//       <GreetingCard name="Alice" />
//       <GreetingCard name="Bob" message="Good day" />
//       <GreetingCard /> // This will show the error message
//     </div>
//   );
// }

// export default App;
*/

export default GreetingCard; 