import * as React from 'react';
import { CssVarsProvider, Box, Typography, Input, FormControl, FormLabel } from '@mui/joy';
import Avatar from '@mui/joy/Avatar';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import 'videojs-youtube'; // Import the Video.js YouTube plugin

import logo from './Hierarchical_Solver.jpeg'; // Make sure the path to your logo is correct

// VideoJS component
const VideoJS = (props) => {
  const videoRef = React.useRef(null);
  const playerRef = React.useRef(null);
  const { options, onReady } = props;

  React.useEffect(() => {
    if (!playerRef.current) {
      const videoElement = document.createElement('video-js');
      videoElement.classList.add('vjs-big-play-centered');
      videoRef.current.appendChild(videoElement);

      const player = playerRef.current = videojs(videoElement, options, () => {
        console.log('player is ready');
        onReady && onReady(player);
      });
    } else {
      const player = playerRef.current;
      player.autoplay(options.autoplay);
      player.src(options.sources);
    }
  }, [options, onReady]);

  React.useEffect(() => {
    const player = playerRef.current;
    return () => {
      if (player && !player.isDisposed()) {
        player.dispose();
        playerRef.current = null;
      }
    };
  }, []);

  return (
    <div data-vjs-player>
      <div ref={videoRef} />
    </div>
  );
};

export default function App() {
  const videoJsOptions = {
    autoplay: false, // YouTube often has restrictions on autoplay
    controls: true,
    responsive: true,
    fluid: true,
    sources: [{
      src: 'answ_plot.mp4', // YouTube video link
      type: 'video/mp4'
    }]
  };

  const handlePlayerReady = (player) => {
    console.log('player is ready');
    // You can handle other player events here
  };

  const [userInput, setUserInput] = React.useState('');

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleInputSubmit = (event) => {
    if (event.key === 'Enter') {
      console.log(userInput);
      setUserInput('');
    }
  };

  return (
    <CssVarsProvider>
      <Box sx={{ bgcolor: 'background.paper', p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Toolbar with Logo and Avatar */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <img src={logo} alt="HiSolver Logo" style={{ marginRight: '10px', borderRadius: '12px', width: '50px', height: '50px' }} />
          <Typography level="h1" component="div" sx={{ fontSize: '1.3rem' }}>
            HiSolver
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography level="body1" sx={{ marginRight: '10px' }}>
            Anonymous
          </Typography>
          <Avatar src="https://image.lexica.art/full_webp/671760b0-293a-4139-bdb6-dfbefe4a077a" alt="User Avatar" />
        </Box>
      </Box>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        {/* Video.js Player */}
        <VideoJS options={videoJsOptions} onReady={handlePlayerReady} />
        {/* User Input Field */}
        <FormControl sx={{ position: 'absolute', bottom: 0, left: 0, right: 0, padding: '16px' }}>
          <Input
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={handleInputSubmit}
            placeholder="What do you want to animate?"
            sx={{ border: 'none', bgcolor: 'background.body' }}
          />
        </FormControl>
      </Box>
    </CssVarsProvider>
  );
}
