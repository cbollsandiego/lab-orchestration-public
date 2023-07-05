import GroupSet from './components/GroupSet.js'
export default {
    delimiters: ["[[", "]]"],
    components: {
        GroupSet
    },
    data() {
        return {
            message: 'Rendering from Vue',
        }
    },
    template: 
    `
    [[ message ]]
    <group-set></group-set>
    `,
    mounted() {
        this.$socket.on('flask_ping', () => {
            console.log('ping');
        });
    }
}