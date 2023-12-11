import * as React from 'react';
import { CssVarsProvider, Box, Typography, FormControl, Input, Avatar, Button, Sheet } from '@mui/joy';
import SendIcon from '@mui/icons-material/Send';
import logo from './Hierarchical_Solver.jpeg';
import video from './Intro.mp4';

export default function App() {
  const [userInput, setUserInput] = React.useState('');
  const [videoSrc, setVideoSrc] = React.useState(video);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const fetchAnimation = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/animation_from_question?query=${encodeURIComponent(userInput)}`);

      if (response.ok) {
        const videoUrl = await response.url;
        setVideoSrc(videoUrl);
      } else {
        console.error('Server responded with error:', response);
      }
    } catch (error) {
      console.error('Error making the request:', error);
    }
  };

  const handleSend = () => {
    if (userInput.trim()) {
      fetchAnimation();
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <CssVarsProvider>
      <Box sx={{ bgcolor: 'background.white', p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Left side: Logo and Text */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <img src={logo} alt="HiSolver Logo" style={{ marginRight: '10px', borderRadius: '12px', width: '50px', height: '50px' }} />
          <Typography level="h1" component="div" sx={{ fontSize: '1.3rem' }}>
            HiSolver MathChat
          </Typography>
        </Box>

        {/* Right side: Username and User Avatar */}
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
          height: '80vh',
        }}
      >
        {/* Video Container */}
        <Sheet sx={{ mb: 2, maxWidth: 800, width: '100%' }}>
          <video controls loop autoPlay muted style={{ width: '100%', height: 'auto', borderRadius: '18px' }} key={videoSrc}>
            <source src={videoSrc} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </Sheet>
        
        {/* Input Field with Send Button */}
        <FormControl sx={{ width: '40%', maxWidth: '800px', marginTop: '20px' }}>
          <Input
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            endDecorator={
              <Button
                size="sm"
                variant="solid"
                sx={{
                  bgcolor: '#4A148C',
                  height: '33px',
                  width: '33px',
                  color: 'white',
                  borderRadius: '10px',
                  '&:hover': { bgcolor: '#6A1B9A' }
                }}
                onClick={handleSend}
              >
                <SendIcon />
              </Button>
            }
            sx={{ height: '50px', borderRadius: '12px', paddingRight: '18px' }}
            placeholder="What do you want to animate?"
            fullWidth
          />
        </FormControl>
      </Box>
    </CssVarsProvider>
  );
}
