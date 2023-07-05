<template>
    <h3>{{ name }} ({{groupId}})</h3>
    <div v-for="member in members">
        {{ member }}
    </div>
    <p v-show="handRaised">
        <i>Hand Raised</i>
    </p>
    <p v-show="atCheckpoint">
        <i>At checkpont!</i>
    </p>
    <p>
        <b>{{ progress }}/{{ maxProgress }}</b>
    </p>
</template>

<script>
export default {
    name: 'GroupInfo',
    props: {
        name: {type: String},
        members: {type: Array},
        maxProgress: {type: Number, default: 0},
        groupId: {type: Number},
        score: {type: Number},
        handRaised: {type: Boolean},
        atCheckpoint: {type: Boolean},
        progress: {type: Number}
    }
}
</script>