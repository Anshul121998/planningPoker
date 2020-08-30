<template>
  <div class="CreateRoom">
    <br />
    <v-snackbar v-model="snackbar" :color="alertColor" timeout="6000" top right>
      {{ alertText }}
      <template v-slot:action="{ attrs }">
        <v-btn dark text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
    <v-overlay :value="isLoading" opacity="0.20">
      <v-progress-circular
        :size="100"
        :width="7"
        color="indigo"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <div v-if="permanentRoomID === ''">
      <br />
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" class="elevation-6" dark flat>
                <v-toolbar-title>CREATE/ENTER ROOM</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    label="Room Creator Name"
                    name="name"
                    prepend-icon="mdi-account"
                    type="text"
                    v-model="pName"
                    :rules="[() => !!pName || 'this field is required']"
                    required
                  ></v-text-field>
                  <br />
                  <h3>OR</h3>
                  <br />
                  <v-text-field
                    label="Enter Existing Room"
                    name="roomId"
                    hint="(Leave empty to create new room ID)"
                    :persistent-hint="true"
                    prepend-icon="mdi-numeric"
                    type="text"
                    v-model="roomId"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" :disabled="allOkay" @click="sendCreatorData()" class="mb-2 mt-2 md-4 ml-12">Create/Enter Room</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div v-else>
      <v-toolbar dense flat style="padding-top:5px">
        <h4>Room ID-</h4>
        <v-btn
          class="ma-2"
          tile
          outlined
          color="black"
          @click="copyToClipBoard()"
        >
          {{ permanentRoomID }}
          <v-icon right>mdi-checkbox-multiple-blank-outline</v-icon>
        </v-btn>
        <h5 v-if="copiedVal">Copied!</h5>
        <v-spacer></v-spacer>
        <v-btn @click="togglePolling()">
          {{ estimateToggle }}
        </v-btn>
      </v-toolbar>
      <div v-if="showPollingList" style="padding-left: 15px">
        <br />
        <h4>Participants who have submitted their estimates -</h4>
        <br />
        <ul>
          <li v-for="(user, index) in currentUserList" :key="index">
            {{ user }}
          </li>
        </ul>
      </div>
      <div v-if="tableData">
        <br />
        <h2 class="deep-purple darken-3" style="color: white; padding-left: 5px padding-right: 5px">
          <center>
            '{{ estimatorSelected }}' please tell why you gave '{{ estimateSelected }}' as estimate
          </center>
        </h2>
        <br />
        <h2><center>Table containing all participants estimate</center></h2>
        <v-data-table
          :headers="headers"
          :items="attendees"
          item-key="name"
          class="elevation-1"
        ></v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import CreateRoomService from '@/services/CreateRoomService.js'
export default {
  name: 'CreateRoom',
  watch: {
    pName: function (val) {
      if (val !== '') {
        this.allOkay = false
      } else {
        this.allOkay = true
      }
    }
  },
  data: () => ({
    isLoading: false,
    roomId: '',
    pName: '',
    alertColor: 'info',
    snackbar: false,
    alertText: '',
    allOkay: true,
    permanentRoomID: '',
    pollingToggle: false,
    estimateToggle: '',
    tableData: false,
    currentUserList: [],
    headers: [
      {
        text: 'Participant Name',
        align: 'start',
        value: 'name'
      },
      {
        text: 'Estimate Given',
        value: 'estimate'
      }
    ],
    attendees: [],
    estimatorSelected: '',
    estimateSelected: '',
    copiedVal: false,
    showPollingList: false
  }),
  methods: {
    sendCreatorData () {
      var data = {}
      data['uuid'] = this.roomId
      data['name'] = this.pName
      data['datetime'] = new Date().toLocaleString()
      this.isLoading = true
      var self = this
      CreateRoomService.createRoom(data).then(
        (response) => {
          if (response.uuid === '1') {
            self.alertColor = 'error'
            self.alertText = 'Room ID does not exist!'
          } else {
            self.alertColor = 'success'
            self.alertText = 'Successfully room created/entered.'
            self.permanentRoomID = response.uuid
            self.pollingToggle = response.polling
            self.estimateToggleValue(response.polling)
          }
          self.snackbar = true
          self.isLoading = false
        },
        () => {
          self.alertColor = 'error'
          self.alertText = 'Error occurred, reload Page!'
          self.snackbar = true
          self.isLoading = false
        }
      )
    },
    estimateToggleValue (data) {
      if (data) {
        this.estimateToggle = 'Close polling and get estimates'
      } else {
        this.estimateToggle = 'New Polling'
      }
    },
    polledUsers () {
      var data = {}
      data['uuid'] = this.permanentRoomID
      var self = this
      CreateRoomService.getCurrUsers(data).then((response) => {
        self.currentUserList = response
        if (self.currentUserList) {
          setTimeout(self.polledUsers(), 150000)
        } else {
          self.currentUserList = []
        }
      })
    },
    copyToClipBoard () {
      var dummy = document.createElement('textarea')
      document.body.appendChild(dummy)
      dummy.value = this.permanentRoomID
      dummy.select()
      document.execCommand('copy')
      document.body.removeChild(dummy)
      this.alertColor = 'success'
      this.alertText = 'Room ID copied successfully.'
      this.snackbar = true
      this.copiedVal = true
    },
    togglePolling () {
      this.tableData = false
      this.isLoading = true
      var data = {}
      data['uuid'] = this.permanentRoomID
      data['polling'] = !this.pollingToggle
      this.isLoading = true
      var self = this
      CreateRoomService.togglePolling(data).then(
        (response) => {
          if (response === 0) {
            self.alertColor = 'error'
            self.alertText = 'Room ID does not exist!'
          } else if (response === 1) {
            self.showPollingList = true
            self.polledUsers()
            self.pollingToggle = !self.pollingToggle
            self.estimateToggleValue(self.pollingToggle)
            self.alertColor = 'success'
            self.alertText = 'Polling started successfully.'
          } else {
            self.showPollingList = false
            self.attendees = response.attendees
            self.estimatorSelected = response.topPeople[ Math.floor(Math.random() * response.topPeople.length) ]
            self.estimateSelected = response.topEstimate
            self.pollingToggle = !self.pollingToggle
            self.estimateToggleValue(self.pollingToggle)
            self.tableData = true
            self.alertColor = 'success'
            self.alertText = 'Polling stopped successfully.'
          }
          self.snackbar = true
          self.isLoading = false
        },
        () => {
          self.alertColor = 'error'
          self.alertText = 'Error occurred, reload Page!'
          self.snackbar = true
          self.isLoading = false
        }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
.CreateRoom {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
h4 {
  display: inline-block;
}
h3 {
  overflow: hidden;
  text-align: center;
}
h3:before,
h3:after {
  background-color: #d3d3d3;
  content: "";
  display: inline-block;
  height: 1px;
  position: relative;
  vertical-align: middle;
  width: 50%;
}
h3:before {
  right: 0.5rem;
  margin-left: -50%;
}
h3:after {
  left: 0.5rem;
  margin-right: -50%;
}
</style>
