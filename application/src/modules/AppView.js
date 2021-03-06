import React, {PropTypes} from 'react';
import {View, StyleSheet, ActivityIndicator, Alert} from 'react-native';
import NavigationViewContainer from './navigation/NavigationViewContainer';
import AppRouter from './AppRouter';
import * as auth0 from '../services/auth0';
import * as snapshotUtil from '../utils/snapshot';
import * as SessionStateActions from '../modules/session/SessionState';
import store from '../redux/store';
import DeveloperMenu from '../components/DeveloperMenu';
import PushNotification from 'react-native-push-notification';
import * as PushNotificationsState from './push-notifications/PushNotificationsState';

const AppView = React.createClass({
  propTypes: {
    isReady: PropTypes.bool.isRequired,
    isLoggedIn: PropTypes.bool.isRequired,
    dispatch: PropTypes.func.isRequired
  },
  componentDidMount() {
    snapshotUtil.resetSnapshot()
      .then(snapshot => {
        const {dispatch} = this.props;

        if (snapshot) {
          dispatch(SessionStateActions.resetSessionStateFromSnapshot(snapshot));
        } else {
          dispatch(SessionStateActions.initializeSessionState());
        }

        store.subscribe(() => {
          snapshotUtil.saveSnapshot(store.getState());
        });
      });

      PushNotification.configure({
        onRegister: ((token) => {
          this.props.dispatch(PushNotificationsState.didReceiveMobileNotificationKey(token.token, token.os));
        }),
        onNotification: ((notification) => {
          Alert.alert('New Notification', notification.message);
        }),
        popInitialNotification: true,
        requestPermissions: true
      });
  },

  componentWillReceiveProps({isReady, isLoggedIn}) {
    if (!this.props.isReady) {
      if (isReady && !isLoggedIn) {
        auth0.showLogin();
      }
    }
  },

  render() {
    if (!this.props.isReady) {
      return (
        <View>
          <ActivityIndicator style={styles.centered}/>
        </View>
      );
    }

    return (
      <View style={{flex: 1}}>
        <NavigationViewContainer router={AppRouter} />
        {__DEV__ && <DeveloperMenu />}
      </View>
    );
  }
});

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    alignSelf: 'center'
  }
});

export default AppView;
