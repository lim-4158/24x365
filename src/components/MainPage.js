// MainPage.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
import ChatComponent from './ChatComponent';
import GoogleSignInButton from './GoogleSignInButton';
import UserCalendar from './UserCalendar';
import EventChecklist from './EventChecklist';
import './MainPage.css';

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
      <div className="tabs-container">
        <Tabs>
          <TabList>
            <Tab>ChatBot</Tab>
            <Tab>User Calendar</Tab>
            <Tab>Event Checklist</Tab>
            <Tab>Reconnect with Google</Tab>
          </TabList>

          <TabPanel>
            <ChatComponent />
          </TabPanel>
          <TabPanel>
            <UserCalendar />
          </TabPanel>
          <TabPanel>
            <EventChecklist />
          </TabPanel>
          <TabPanel>
            <GoogleSignInButton />
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
};

export default MainPage;
