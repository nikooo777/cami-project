import {Map} from 'immutable';
import React, {PropTypes} from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
} from 'react-native';
import Color from 'color';
import moment from 'moment';

import StatusEntry from './components/StatusEntry';

const StatusView = React.createClass({
  propTypes: {
    username: PropTypes.string.isRequired,
    status: PropTypes.instanceOf(Map).isRequired
  },

  render() {
    console.log('status:', this.props.status);

    return (
      <View style={styles.container}>
        <View style={styles.iconContainer}>
          <Text style={[styles.mainText, {fontWeight: 'bold'}]}>
            Status
          </Text>
        </View>

        <ScrollView>
          <StatusEntry
            type="heart"
            status={this.props.status.get('heart').get('status')}
            data={this.props.status.get('heart').get('data')}
          />
        </ScrollView>
      </View>
    );
  }
});

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'moccasin'
  },
  iconContainer: {
    // flex: 1,
    backgroundColor: '#658d51',
    zIndex: 2,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 20
  },
  mainText: {
    fontSize: 26,
    color: 'white',
    lineHeight: 1.3*26
  },
});

export default StatusView;
