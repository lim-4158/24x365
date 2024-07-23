import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import ChatComponent from './ChatComponent';
import GoogleSignInButton from './GoogleSignInButton';
import UserCalendar from './UserCalendar';
import EventChecklist from './EventChecklist';

const MainPage = () => {
  const navigate = useNavigate();

  // Function to check if the user is authenticated
  const isAuthenticated = () => {
    const token = localStorage.getItem('token');
    return token !== null;
  };

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login'); // Redirect to login page if not authenticated
    }
  }, [navigate]);

  return (
    <div className="main-page-container">
      <Tabs>
        <TabList>
          <Tab>ChatBot</Tab>
          <Tab>Google Sign-In</Tab>
          <Tab>User Calendar</Tab>
          <Tab>Event Checklist</Tab>
        </TabList>

        <TabPanel>
          <ChatComponent />
        </TabPanel>
        <TabPanel>
          <GoogleSignInButton />
        </TabPanel>
        <TabPanel>
          <UserCalendar />
        </TabPanel>
        <TabPanel>
          <EventChecklist />
        </TabPanel>
      </Tabs>
    </div>
  );
};

export default MainPage;
